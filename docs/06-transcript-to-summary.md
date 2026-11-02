# 6. From Transcript to Summary

You have a clean, speaker-labeled transcript. Now the fun part: turn 9,000 words into a half-page of actual value — an outline, decisions, action items — using a language model that runs **on your own machine**, with **no API key**, through a plain OpenAI-compatible endpoint.

## The setup: any OpenAI-compatible endpoint, zero keys

"OpenAI-compatible" is just a URL convention: anything that accepts a `POST /v1/chat/completions` with a JSON body and answers with JSON. Lots of software speaks it:

| Software | Default `base_url` | Does it need a key? |
| --- | --- | --- |
| **Ollama** (the default here) | `http://localhost:11434/v1` | **No.** Any dummy string ("ollama") works as the key and is ignored. |
| LM Studio | `http://localhost:1234/v1` | No |
| llama.cpp `llama-server` | `http://localhost:8080/v1` | No |
| vLLM, text-generation-webui, KoboldCpp | varies (`/v1`) | No |
| OpenAI/Anthropic/Groq etc. (cloud, not local) | their URLs | Yes — *and that defeats the point* (see [chapter 7](07-what-stays-offline.html)) |

Key insight: **local servers don't authenticate because there's nothing to protect on an open localhost port.** The "Bearer anything" key is a box cloud APIs force you to tick; locally, it's just convention. If a library demands *some* key, type `local`.

### Install Ollama and confirm it works

1. Install from [ollama.com](https://ollama.com) (one installer, Windows/macOS/Linux).
2. `ollama run llama3.2:3b` — pulls a ~2 GB model and opens a chat. Say `hi`, then `/bye`.
3. Confirm the OpenAI-compatible door: `curl http://localhost:11434/v1/models` — you should see a list of models in JSON.

That's the whole infrastructure. Now pick a summarizer model:

| Model | Size | Notes |
| --- | --- | --- |
| `llama3.2:3b` | ~2 GB | The everyday default; runs on almost anything |
| `llama3.1:8b` | ~4.7 GB | Noticeably better summaries if you have 16 GB RAM |
| `qwen2.5:7b` | ~4.7 GB | Strong with non-English transcripts |
| `mistral:7b` | ~4.1 GB | Fast, punchy, good with instructions |

## The workhorse: a tiny no-key summarizer script

This handbook ships one: `scripts/summarize_transcript.py`. It takes a transcript file, sends it to *your* endpoint, and prints the summary. No key required — just a `base_url`:

```bash
# Default: Ollama on this machine
python3 scripts/summarize_transcript.py meeting.txt

# Any other OpenAI-compatible server — just repoint the URL
python3 scripts/summarize_transcript.py meeting.txt --base-url http://localhost:1234/v1 --model qwen2.5:7b
```

Under the hood it's the standard three lines of the OpenAI-compatible world (the script uses plain `urllib`, so it has zero dependencies beyond Python itself):

```python
import json, urllib.request

req = urllib.request.Request(
    base_url + "/chat/completions",
    data=json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
    }).encode(),
    headers={"Content-Type": "application/json"},  # no Authorization header: no key, by design
)
with urllib.request.urlopen(req) as r:
    summary = json.load(r)["choices"][0]["message"]["content"]
```

Everything the model sees — the transcript and the prompt — stays in the request to `localhost`. Nothing leaves your machine unless *you* point `--base-url` at a cloud API.

## The two-sentence prompt that does 80% of the work

```
Summarize this transcript. Keep the speakers' own wording when quoting.
Return: (1) a 5-bullet overview, (2) decisions made, (3) open questions,
(4) action items with owners if names were mentioned.
```

Four sections, in that order, covers almost every meeting/interview/lecture. The "keep the speakers' own wording" clause is the [cleanup chapter's](04-cleanup-rules.html) hard rule arriving at the LLM: no paraphrase-into-generic-corporate-speak.

For a cleanup-assist job instead of a summary (the LLM tidying punctuation/fillers *without* touching voice), swap the prompt:

```
Clean this transcript for readability. Rules, in bold so they can't be missed:
**Never replace a word with another word. Never change dialect, pet phrases,
or slang. You may delete fillers ("um", "uh") and trim false starts. You may
re-punctuate. Make paragraph breaks by idea. Output only the cleaned text.**
```

(Yes, the demonstration is deliberate: put the rules in **bold**, models follow emphasized rules much more reliably, and the word *never* does more work than a paragraph of politeness.)

## The staged process for long transcripts

One giant "summarize this 90-minute transcript" prompt on a small local model gives mush. Summaries get better in stages:

1. **Stage 1 — outline every chunk.** 15 minutes of transcript at a time (≈ 3,000 tokens, fits any model): "List the main topics discussed in this passage, one line each, with a rough timestamp if present."
2. **Stage 2 — the outline of outlines.** Paste all chunk-outline outputs together: "Merge these into a single outline of the whole recording."
3. **Stage 3 — targeted pulls.** Paste the Stage 2 outline into a prompt with your actual question: "Below is an outline of a recording. Where is the budget discussion? Quote the exact 2–3 sentences where the decision was made." Then *you* do the [verbatim check](04-cleanup-rules.html) on the quoted text.
4. **Stage 4 — craft the deliverable** yourself. The model proposes; a human edits. A summary whose final 10% is human reasoning reads like a person; one that is 100% model reads like a template.

## Context-window math, done for you

The arithmetic that decides whether this works on a given model:

- 1 hour of speech ≈ 9,000 words ≈ **~12,000 tokens** ([the size chapter](03-file-formats-size-math.html)).
- Ollama's default context window is 4,096 tokens, deliberately small for memory safety. A 1-hour transcript *will not fit* in the default window, and Ollama will silently truncate the *end* of your transcript. This is the silent failure that makes people decide "local models are dumb" when the model simply never saw the last 2/3 of the meeting.
- Fix it with a request parameter (this script does it): send `num_ctx`/`context_length` 16384 or 32768, i.e., a roomy window. The `llama3.2:3b` model handles 32k comfortably on 8 GB machines.
- Still too long? Use the [staged process](#the-staged-process-for-long-transcripts) above; chunk-then-merge also produces better outlines than a single mega-prompt.

## Decisions and action items: the highest-value prompt

For meetings especially, the "what happens next" summary is the one that gets used:

```
From this transcript, extract every decision, commitment, and task.
For each: WHO (name or "unassigned"), WHAT (one sentence, using the speaker's
own wording where possible), and WHEN (date/deadline if stated, else "not stated").
Output as a markdown checklist.
```

Feed that one output straight into your task manager. Combined with labeled speakers ([chapter 5](05-speaker-labeling.html)), the "who" is real names, not "someone."

## What can go wrong (and the fix)

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| Summary only covers the first ~5 min | Context window truncation | Raise context size; or [stage it](#the-staged-process-for-long-transcripts) |
| Invented "decisions" no one made | Model filling in plausible meeting-script content | Ask "quote the exact sentence that decided this" for every item; verify quotes |
| Everything sounds generic | Model paraphrasing into its own voice | Add "preserve speakers' own wording" and quote-everything prompts |
| Model refusals ("I cannot...") | Acting on transcript content it suspects is private/sensitive | Not a cloud-safety thing — local models rarely refuse; if one does, try a different model |
| Endpoint returns 404 | Wrong `base_url` path (some servers want `/v1`, some don't) | Check `/v1/models` with curl first |

## The one-sentence version of this chapter

**Point a `base_url` at any OpenAI-compatible server on your own machine — Ollama by default, no key, no cloud — request by half-hours not by hours, quote rather than paraphrase, and finish the summary yourself.**

Next: drawing the privacy line, on purpose → [What Stays Offline](07-what-stays-offline.html).
