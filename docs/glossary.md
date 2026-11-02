# Glossary

Words this field uses, said the way a friend would.

**Base URL** — The internet address an API lives at, like `http://localhost:11434/v1`. You put it in tools like the summarizer script to decide *which* program will do the work. Change the base URL, change the program — same API shape.

**Bit depth** — Precision of each audio snapshot. 16-bit is the speech standard; higher is only music-relevant.

**Bitrate** — Data-per-second of a compressed audio file, e.g. "64 kbps" = 64,000 bits per second. Pure voice is fine at 64; higher adds music-quality, not speech-clarity.

**Channels** — Independent audio streams. Mono (1) = one mic. Stereo (2) = two mics. Recording one voice in stereo doubles file size for nothing.

**Clean verbatim** — Transcript type where fillers and dry restarts are removed, punctuation fixed, but *no word is swapped for another word*. This handbook's default product.

**Context window** — How much text a language model can consider at once, measured in tokens. Silently too small = silently truncated transcripts (the "model forgot the end of the meeting" bug).

**Diarization** — Automatic speaker identification, splitting a transcript by which voice spoke. Works best in clean two-voice audio; hand-labeling beats it for one messy mic.

**Endpoint** — The full URL of a specific API action, e.g. base URL + `/chat/completions`. The "door" you knock on with a request.

**ffmpeg** — The universal audio/video conversion command-line tool. Every flag in this handbook (`-ac`, `-ar`, `-ss`, `-af silenceremove`) is ffmpeg.

**FLAC** — Lossless compressed audio: identical sound to WAV at roughly half the size. Good archive format.

**Filler** — Speech padding like "um," "uh," "like." Removable in clean verbatim; keep dialect and pet phrases, which are *voice*, not noise.

**Hallucination (STT)** — When a transcriber invents fluent text over silence/noise — most often boilerplate like "Thanks for watching!" Whisper's best-known quirk; fix by trimming silences and short clips.

**kHZ (kilohertz)** — Thousands of samples per second. Speech capture standard is 16 kHz sample rate; audio-CD standard is 44.1 kHz.

**LLM (Large Language Model)** — The text model behind summarizers. Runs locally (Ollama, LM Studio) or in the cloud (OpenAI etc.).

**lmstudio / llama.cpp server** — Alternative local apps to run an LLM behind an OpenAI-compatible API, if Ollama isn't your style. Same API shape; different server software.

**Mono** — Single channel. Record voice in mono unless you know you need stereo.

**num_ctx / context_length** — The request parameter (Ollama: `num_ctx`) that sets a model's context window for a given request. Bump it to 16k/32k for hour-long transcripts.

**OpenAI-compatible API** — The URL+JSON request/response shape made standard by OpenAI and now adopted everywhere, including fully local tools. Lets you swap engines by changing one URL, no key needed locally.

**Ollama** — The app that runs an LLM locally and exposes it at `http://localhost:11434/v1`. Default summarizer backend for this handbook.

**Opus / OGG** — Modern speech-friendly codecs, smaller than MP3 at equal quality. Fine, but MP3/M4A are still the universal playback formats.

**Sample rate** — Snapshots of sound captured per second, in Hz. 16,000 Hz covers all of human speech; higher rates are for music.

**Token** — Chunk of text (~¾ of a word in English) that is the LLM's unit of counting. A 1-hour speech transcript ≈ 12,000 tokens.

**Transcript proportions** — 1 hour of speech ≈ 9,000 words ≈ ~55 KB of text, vs ~30–115 MB of the audio. Text is 2,000× lighter — which is why keeping transcripts forever is free.

**Verbatim** — Transcript type preserving everything including fillers and stumbles, used for legal/ethnographic accuracy. Contrast with clean verbatim.

**whisper.cpp** — The one-binary terminal implementation of Whisper models. The "one command" recommended path in this handbook.

**Whisper (variants)** — OpenAI's open transcription model, reused by whisper.cpp, faster-whisper, and the original Python implementation. Same model file, different runners.
