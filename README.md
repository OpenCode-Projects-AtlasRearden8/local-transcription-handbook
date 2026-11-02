# Local Transcription Handbook

*Turn any recording into clean, readable text — on your own machine, with free tools, no subscriptions, and no API keys.*

A plain-English manual covering the whole path from microphone to summary:

1. **[Record Smart](https://dylanasdale.github.io)** — rooms, phones, and pocket recorders; why mic distance beats every setting.
2. **Free local speech-to-text, compared honestly** — whisper.cpp / faster-whisper / Vosk / pocketsphinx, with the trade-offs marketing pages skip (hallucinations over silence, no punctuation, setup weight).
3. **File formats and the size math** — why a 2-hour meeting is ~58 MB as MP3 and ~2 GB as stereo WAV, and why the transcript of it is ~50 KB (a ~2,000× collapse).
4. **Cleanup rules that keep the speaker's voice** — the verbatim vs. clean-verbatim line, and the one hard rule: *never swap a word for a word*.
5. **Hand-labeling speakers** — a realistic workflow for "who said that?" on a single mic, and when automatic diarization is and isn't worth it.
6. **Transcript → summary** — with a zero-dependency script that talks to any OpenAI-compatible endpoint. **Ollama by default** (`http://localhost:11434/v1`), any `base_url` you point it at, **no API key** — local servers don't authenticate.
7. **What stays offline** — an explicit privacy policy: everything before "publish" happens on your machine; audio never has to leave it.

Plus a printable **[Workflow Sheet](docs/workflow-sheet.md)** and a **[Glossary](docs/glossary.md)**.

**By [Asdale Dynamics, LLC](https://dylanasdale.github.io)** — beginner-friendly AI education: plain English, step by step, never condescending. Companion to the *voice-notes-transcriber-cli* tool (which this manual explains the ideas behind) and distinct from the *audiobook-recording-handbook* (which produces audio people listen to; this one produces text people read).

## Quick start

Build the static HTML site from the Markdown source:

```bash
python3 build.py                # builds into ./site
python3 build.py --out mydir    # or anywhere else
```

Then open `site/index.html` in a browser, or just read the files in [`docs/`](docs/) directly.

Run the built-in summarizer against a local LLM endpoint (requires an OpenAI-compatible server such as [Ollama](https://ollama.com) running):

```bash
python3 scripts/summarize_transcript.py transcript.txt
# repoint at any other OpenAI-compatible server:
python3 scripts/summarize_transcript.py transcript.txt --base-url http://localhost:1234/v1 --model qwen2.5:7b
# other tasks: --task summary|actions|outline|cleanup
```

The script uses only Python's standard library — no pip installs, no keys. Everything it sends stays on the machine the `base_url` points at; the default sends it nowhere but `localhost`.

## Repository layout

```
docs/        the handbook, chapter by chapter (markdown, readable on GitHub)
site/        built static HTML (rebuildable; see build.py)
build.py     markdown → static site with navigation, prev/next, and link checking
scripts/     summarize_transcript.py — the no-key local LLM summarizer
tests/       pytest suite (docs integrity, build correctness, script behavior)
```

## Tests

```bash
python3 -m pytest
```

The suite verifies: every expected chapter exists and cross-links resolve, the build produces a complete site (including prev/next navigation and a failure on broken internal links), no secrets in committed files, and the summarizer script — both unit-level (payload shape, no `Authorization` header, Ollama context bumping, chunking/merging) and end-to-end against a real local HTTP server that stands in for an OpenAI-compatible endpoint.

## Documentation map

| Read as... | Start at |
| --- | --- |
| "I have a recording, now what?" | [Workflow Sheet](docs/workflow-sheet.md) |
| "I want to understand each step" | [Chapter 1 — Record Smart](docs/01-record-smart.md) |
| "I want the honest tool comparison" | [Chapter 2 — Local STT, Compared](docs/02-local-stt-options.md) |
| "Is my audio private?" | [Chapter 7 — What Stays Offline](docs/07-what-stays-offline.md) |

## License

MIT — see [LICENSE](LICENSE). Copyright (c) 2026 Asdale Dynamics, LLC.

*This handbook is education, not legal or professional advice; it never handles your audio remotely because it never touches your audio at all.*
