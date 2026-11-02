# STATUS.md — local-transcription-handbook

Last updated: 2026-11-01

## What was built

**Local Transcription Handbook** — a beginner-friendly manual for turning recorded audio into clean text on your own machine, by Asdale Dynamics, LLC. Markdown sources build (via a tested script) into a static HTML site.

Deliverables against the original goal:

- **Record smart** (`docs/01-record-smart.md`) — rooms, phones, pocket recorders; proximity-first recording doctrine; pre-flight checklist.
- **Free local speech-to-text, compared honestly** (`docs/02-local-stt-options.md`) — whisper.cpp / faster-whisper / OpenAI Whisper / Vosk / pocketsphinx, with the trade-offs usually skipped (hallucination over silence, missing punctuation in Vosk, setup weight, model-vs-tool reality).
- **File-format and size math** (`docs/03-file-formats-size-math.md`) — the four numbers behind file size, MB-per-minute cheat sheet, the ~2,000× audio→text collapse, ffmpeg recipes.
- **Cleanup rules that keep the speaker's voice** (`docs/04-cleanup-rules.md`) — verbatim vs. clean verbatim, the hard "never swap a word for a word" rule, Whisper-shaped fixes, a tiered cleanup ladder.
- **Hand-labeling speakers** (`docs/05-speaker-labeling.md`) — honest take on diarization, timestamped labeling workflow, uncertainty policy (`UNKNOWN (ts)`), multi-track alternatives.
- **Transcript → summary** (`docs/06-transcript-to-summary.md`) — any OpenAI-compatible endpoint, **Ollama default** (`http://localhost:11434/v1`), any `base_url`, **no API keys**; staged summarization for long transcripts; context-window math; the decisions/action-items prompt.
- **What stays offline** (`docs/07-what-stays-offline.md`) — explicit per-step privacy policy with honest exceptions.
- **Workflow sheet** (`docs/workflow-sheet.md`) — one printable page: pre-record checklist → transcribe → clean → label → summarize → privacy checkpoint.
- **Glossary** (`docs/glossary.md`) — jargon in plain English.
- **`scripts/summarize_transcript.py`** — runnable summarizer using only the Python stdlib; tasks `summary|actions|outline|cleanup`; chunk-and-merge for long transcripts; sends no `Authorization` header (no key by design); `--base-url` repoints at any OpenAI-compatible server, default Ollama.
- **`build.py`** — markdown → static HTML site (sidebar nav with filter, prev/next pager, print styles, internal-link checking that fails the build on dead links).
- **`tests/`** — pytest suite (26 tests).
- **`site/`** — freshly built static HTML committed for direct browsing.

Distinct on purpose from *voice-notes-transcriber-cli* (a one-command tool; this is the manual behind it) and *audiobook-recording-handbook* (producing audio to listen to; this produces text to read).

## How to run it

```bash
# build the static site
python3 build.py                  # -> ./site, open site/index.html

# run the tests
python3 -m pytest

# summarize a transcript locally (requires Ollama running with a model pulled)
python3 scripts/summarize_transcript.py transcript.txt
# any other OpenAI-compatible endpoint:
python3 scripts/summarize_transcript.py transcript.txt --base-url http://localhost:1234/v1 --model qwen2.5:7b
```

Requirements: Python 3.10+ and the `markdown` package for `build.py`; nothing beyond stdlib for `scripts/summarize_transcript.py`; an OpenAI-compatible local server (Ollama/LM Studio/llama-server) if you run the summarizer for real.

## Verification results

- `python3 build.py` — **pass**: builds 10 pages; internal-link check passes (all chapter cross-links and heading anchors resolve).
- `python3 -m pytest` — **pass: 26/26**
  - docs integrity: all chapters exist, index links every chapter, no TODO/TBD placeholders, no secrets in committed files.
  - build correctness: full page set produced, stale outputs removed, nav/pager present, broken internal links and missing pages fail the build, CLI exit code 0.
  - summarizer: chunking math, prompt templates, no-`Authorization`-header guarantee (payload inspected), Ollama `num_ctx` context bump, friendly failure hints; two end-to-end tests run the script via subprocess against a real local HTTP server standing in for `/v1/chat/completions` (single-shot and chunk-merge paths).
- Summarizer was additionally exercised manually against the mock server; not run against a live model install in this environment (none available offline).

## License / attribution

- `LICENSE`: MIT, `Copyright (c) 2026 Asdale Dynamics, LLC`.
- README credits and links Asdale Dynamics, LLC.

## Known gaps

- **No live speech-to-text is bundled** — the handbook teaches whisper.cpp/faster-whisper usage but does not vendor model weights or an install script (deliberate: keeps the repo dependency-free and small).
- **No automatic diarization guide in depth** — chapter 5 recommends hand-labeling for one-mic recordings and points at multi-track alternatives; a dedicated `pyannote` walkthrough would be a natural follow-up.
- **Site search is nav-label filtering only** — full-text site search is a possible future upgrade.
- **Sample audio + transcript pair** for practicing the cleanup chapter is not included (would add binary files; may add a tiny synthetic one later).
- **`site/` is committed**; remember to rebuild it after editing `docs/` (`python3 build.py`).
