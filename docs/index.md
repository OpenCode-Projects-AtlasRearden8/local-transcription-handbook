# Local Transcription Handbook

Turn any recording — a meeting, an interview, a lecture, a voice memo — into clean, readable text on your own machine. No subscriptions, no uploading audio to strangers, no monthly fee.

This manual is written the way I'd explain it to a friend: plain English, one step at a time, and honest about what's easy, what's annoying, and what free tools genuinely can't do yet.

**By [Asdale Dynamics, LLC](https://dylanasdale.github.io) — beginner-friendly AI education, local-first by default.**

## What you'll learn

1. **Record smart.** How rooms, phones, and pocket recorders behave, so the hard work happens before you press record. See [Record Smart](01-record-smart.html).
2. **Pick a free local speech-to-text tool.** Whisper variants, Vosk, and friends — compared honestly, including the parts a marketing page would leave out. See [Free Local Speech-to-Text, Compared](02-local-stt-options.html).
3. **Do the file-format and size math.** Why a 2-hour recording is ~115 MB as WAV but ~30 MB as MP3, why audio shrinks 2,000× when it becomes text, and what your disk actually needs. See [File Formats and the Size Math](03-file-formats-size-math.html).
4. **Clean up the transcript without wrecking the voice.** Rules for fixing punctuation and stumbles while keeping how the person actually talks. See [Cleanup Rules That Keep the Speaker's Voice](04-cleanup-rules.html).
5. **Identify and label speakers by hand.** A realistic workflow for "who said that?" on a single-mic recording. See [Hand-Labeling Speakers](05-speaker-labeling.html).
6. **Turn a transcript into a summary.** Using any OpenAI-compatible endpoint — Ollama by default, any `base_url` you point it at, no API keys. See [From Transcript to Summary](06-transcript-to-summary.html).
7. **Decide what stays offline.** A simple policy for keeping audio private, and the rare cases where online tools earn their keep. See [What Stays Offline](07-what-stays-offline.html).
8. **One-page [Workflow Sheet](workflow-sheet.html)** you can keep next to your recorder, and a **[Glossary](glossary.html)** for the jargon.

## Who this is for

Anyone who records audio and wants the words: students, journalists, nurses documenting in-service trainings, small-business owners, podcasters, movers of estates and resellers dictating item notes, and anyone whose brain works better out loud than on a keyboard.

## How this differs from our other projects

- **[voice-notes-transcriber-cli](https://github.com/dylanasdale)** is a *tool*: one command that transcribes a file or folder for you. This handbook is the *manual*: it explains the ideas, the comparisons, and the cleanup craft, so you can use that tool or any setup like it with confidence.
- **audiobook-recording-handbook** is about *producing* audio people listen to. This handbook is about *reading* audio as text.

They share a philosophy — local-first, free tools, plain English — but not their subject. If you just want one command that works, use the CLI tool. If you want to understand and steer every step, this is your book.

## What you'll need

- Any computer (Windows, Mac, or Linux) with 4 GB of RAM to spare while transcribing; 8 GB is comfortable.
- Optional but recommended: an NVIDIA graphics card or an Apple Silicon Mac, which makes transcription much faster.
- Nothing else. Every tool in this handbook is free, and nothing requires an internet connection after setup.

## The one-paragraph version

Record well with whatever you have, in the best corner of the room with the mic close-ish to the talker. Run the audio (WAV or MP3, mono, 16 kHz) through a local Whisper model — `base` size is the sweet spot for English. Tidy the output with a light editorial hand: fix the punctuation, keep the person. Label speakers by hand because that's still more reliable than free automatic tools for a single mic. Hand the clean transcript to a summarizer pointed at your own Ollama server (or any OpenAI-compatible `base_url`) with no API key, and get an outline and action items back in the time it takes to refill your coffee.

Start with [Record Smart](01-record-smart.html).
