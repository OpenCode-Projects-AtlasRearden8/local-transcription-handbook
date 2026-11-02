#!/usr/bin/env python3
"""Summarize a transcript with any OpenAI-compatible endpoint — no API key.

Default target is Ollama on this machine (http://localhost:11434/v1), but any
base_url that speaks the OpenAI-style /chat/completions API works, with no
Authorization header: local servers don't authenticate.

Examples:
    python3 scripts/summarize_transcript.py meeting.txt
    python3 scripts/summarize_transcript.py meeting.txt --base-url http://localhost:1234/v1 --model qwen2.5:7b
    python3 scripts/summarize_transcript.py meeting.txt --task actions
    python3 scripts/summarize_transcript.py meeting.txt --task cleanup -o meeting_clean.md
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

DEFAULT_BASE_URL = "http://localhost:11434/v1"
DEFAULT_MODEL = "llama3.2:3b"
DEFAULT_CTX = 16384

PROMPTS = {
    "summary": (
        "Summarize this transcript. Keep the speakers' own wording when quoting. "
        "Return: (1) a 5-bullet overview, (2) decisions made, (3) open questions, "
        "(4) action items with owners if names were mentioned.\n\nTRANSCRIPT:\n{transcript}"
    ),
    "actions": (
        "From this transcript, extract every decision, commitment, and task. "
        "For each: WHO (name or \"unassigned\"), WHAT (one sentence, using the speaker's "
        "own wording where possible), and WHEN (date/deadline if stated, else \"not stated\"). "
        "Output as a markdown checklist.\n\nTRANSCRIPT:\n{transcript}"
    ),
    "outline": (
        "List the main topics discussed in this transcript, one line each, "
        "with a rough timestamp if one is present.\n\nTRANSCRIPT:\n{transcript}"
    ),
    "cleanup": (
        "Clean this transcript for readability. Rules, in bold so they can't be missed: "
        "**Never replace a word with another word. Never change dialect, pet phrases, "
        "or slang. You may delete fillers (\"um\", \"uh\") and trim false starts. You may "
        "re-punctuate. Make paragraph breaks by idea. Output only the cleaned text.**\n\n"
        "TRANSCRIPT:\n{transcript}"
    ),
}


def split_chunks(text: str, max_chars: int) -> list[str]:
    """Split long text on paragraph boundaries so each chunk fits one request."""
    if len(text) <= max_chars:
        return [text]
    paragraphs = text.split("\n\n")
    chunks: list[str] = []
    current = ""
    for para in paragraphs:
        if current and len(current) + len(para) + 2 > max_chars:
            chunks.append(current)
            current = para
        else:
            current = f"{current}\n\n{para}" if current else para
    if current:
        chunks.append(current)
    return chunks


def chat(base_url: str, model: str, prompt: str, context_tokens: int, timeout: int) -> str:
    """One POST to /chat/completions. No Authorization header — that's the point."""
    url = base_url.rstrip("/")
    if not url.endswith("/chat/completions"):
        url += "/chat/completions"
    payload: dict = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
    }
    if "11434" in base_url:  # Ollama: ask for a roomy context window explicitly
        payload["options"] = {"num_ctx": context_tokens}
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.load(resp)
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")[:400]
        raise SystemExit(f"Server error {e.code}: {detail}\nDid you check the base_url? Try: curl {base_url.rstrip('/')}/models") from None
    except urllib.error.URLError as e:
        raise SystemExit(
            f"Could not reach {base_url} ({e.reason}).\n"
            "Is your local server running? For the default: 'ollama serve' (or the Ollama app),\n"
            "and pull a model first: ollama pull llama3.2:3b"
        ) from None
    try:
        return data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError) as e:
        raise SystemExit(f"Unexpected response shape from server: {json.dumps(data)[:400]}") from e


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Summarize a transcript via an OpenAI-compatible endpoint (no API key)")
    ap.add_argument("transcript", help="path to a plain-text transcript")
    ap.add_argument("--base-url", default=DEFAULT_BASE_URL, help=f"OpenAI-compatible base URL (default: {DEFAULT_BASE_URL})")
    ap.add_argument("--model", default=DEFAULT_MODEL, help=f"model name as the server knows it (default: {DEFAULT_MODEL})")
    ap.add_argument("--task", default="summary", choices=sorted(PROMPTS), help="what to produce (default: summary)")
    ap.add_argument("--preset", default=None, choices=sorted(PROMPTS), help="alias for --task (kept for convenience)")
    ap.add_argument("--max-chars", type=int, default=40000, help="chunk size in characters for long transcripts")
    ap.add_argument("--context-tokens", type=int, default=DEFAULT_CTX, help="Ollama num_ctx (default: %(default)s)")
    ap.add_argument("--timeout", type=int, default=600, help="seconds per request")
    ap.add_argument("-o", "--output", help="write result to this file instead of stdout")
    args = ap.parse_args(argv)

    if args.preset:
        args.task = args.preset

    path = Path(args.transcript)
    if not path.is_file():
        ap.error(f"no such file: {path}")

    text = path.read_text(encoding="utf-8")
    if not text.strip():
        ap.error("transcript file is empty")

    prompt_tmpl = PROMPTS[args.task]
    chunks = split_chunks(text, args.max_chars)
    results = []
    for i, chunk in enumerate(chunks, 1):
        if len(chunks) > 1:
            print(f"[chunk {i}/{len(chunks)}]", file=sys.stderr)
        results.append(chat(args.base_url, args.model, prompt_tmpl.format(transcript=chunk), args.context_tokens, args.timeout))

    parts = []
    if len(results) > 1 and args.task == "outline":
        # merge stage: outline of outlines
        merged = "\n\n".join(f"--- part {i} ---\n{r}" for i, r in enumerate(results, 1))
        merge_prompt = (
            "Merge these partial outlines of one recording into a single outline, "
            "preserving order.\n\n" + merged
        )
        parts.append(chat(args.base_url, args.model, merge_prompt, args.context_tokens, args.timeout))
    else:
        parts = results

    out_text = "\n\n".join(parts)
    if args.output:
        Path(args.output).write_text(out_text + "\n", encoding="utf-8")
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(out_text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
