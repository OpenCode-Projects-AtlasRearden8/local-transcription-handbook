# 3. File Formats and the Size Math

Understanding a little bit of audio math pays off forever: you'll know how much battery, disk, and setup time a recording costs *before* you press record, and you'll never be confused by the word "bitrate" again.

## The four numbers that actually matter

Every audio file's size comes down to four numbers:

1. **Sample rate** (Hz) — how many snapshots of the sound per second. Human speech matters below ~11,000 Hz; 16,000 Hz captures it all, which is why 16 kHz (16,000 Hz) is the standard for speech.
2. **Bit depth** (bits) — precision of each snapshot. 16-bit is standard and fine.
3. **Channels** — mono (1) or stereo (2). One voice, one mic, mono. Stereo doubles the size for zero benefit when you're recording a single source.
4. **Compression** — none (WAV/PCM), lossy-but-clean (MP3, AAC/M4A, OGG), or lossless-but-smaller (FLAC).

## The formula

**Size (bytes/second) = sample rate × bit depth ÷ 8 × channels × compression ratio**

Uncompressed WAV has a ratio of 1. MP3 at 128 kbps compresses roughly 11:1 from 44.1 kHz stereo WAV (less from 16 kHz mono).

## Cheat sheet: MB per minute

| Format | Typical use | Size per minute | Size per hour |
| --- | --- | --- | --- |
| WAV, 44.1 kHz, 16-bit, stereo | CD-quality reference | ~10.6 MB | ~0.6 GB |
| WAV, 44.1 kHz, 16-bit, **mono** | One mic, raw capture | ~5.3 MB | ~0.3 GB |
| **WAV, 16 kHz, 16-bit, mono** | The speech-to-text standard | ~1.9 MB | ~115 MB |
| MP3, 128 kbps | Voice podcast/class | ~0.96 MB | ~58 MB |
| **MP3, 64 kbps mono** | Spoken word | ~0.48 MB | **~29 MB** |
| MP3, 32 kbps mono | Bare-minimum speech | ~0.24 MB | ~14 MB |
| AAC/M4A (iPhone voice memo) | Phone default | ~0.5–1 MB | ~30–60 MB |
| Opus/OGG, 48 kbps | Voice-first modern codec | ~0.36 MB | ~22 MB |

Worked examples of the formula:

- WAV 16 kHz mono 16-bit: 16,000 × 16 ÷ 8 × 1 = **32,000 bytes/sec** = 32 KB/s ≈ 1.9 MB/min ≈ 115 MB/hr.
- MP3 64 kbps: 64,000 bits/sec ÷ 8 = 8,000 bytes/sec = 8 KB/s ≈ 0.48 MB/min ≈ **29 MB/hr**.

Phones and recorders rarely shoot over 128 kbps for voice — the extras are "music headroom" you don't need. A 90-minute meeting as 64 kbps mono MP3 is **~43 MB**. Anyone can move that.

## The 2,000× collapse

Here's the beautiful part: **text is microscopically smaller than audio.**

One hour of speech ≈ 9,000 words ≈ ~55 KB of plain text. Compare to **29 MB** (MP3) or **115 MB** (WAV) for that same audio:

| | Audio (1 hour, MP3 64k) | Transcript (of the same hour) |
| --- | --- | --- |
| Size | ~29,000 KB | ~55 KB |
| Ratio | 1 | **~1/530 of MP3, ~1/2,000 of WAV** |

Practical consequences:

- **Gaping disk for transcripts.** Keep every transcript forever; they weigh nothing. The 100-hour corpus of interviews you're hoarding for a book is ~30 GB of (compressed) audio and ~5 MB of text.
- **Formatting adds ~2×, not more.** Timestamped, speaker-labeled transcripts run ~2–3× the raw word count in bytes. Still trivial.
- **LLM summarization math.** A 1-hour transcript ≈ 9,000 words ≈ ~12,000 tokens. That fits *comfortably* in a 32,000-token local model context — chapter 6 builds on this fact.

## Converting between formats

ffmpeg is the universal translator and this handbook's recommendation (also useful for [pre-chunking audio](02-local-stt-options.html) against Whisper hallucination on silence):

```bash
# Any format → 16 kHz mono WAV (the transcription standard)
ffmpeg -i input.m4a -ac 1 -ar 16000 output.wav

# Any format → small speech MP3
ffmpeg -i input.wav -ac 1 -b:a 64k output.mp3

# Trim the first 15 minutes off
ffmpeg -i input.wav -ss 00:15:00 output_trimmed.wav

# Squeeze out long silences (helps against Whisper "hallucinating" text over pauses)
ffmpeg -i input.wav -af silenceremove=stop_periods=-1:stop_duration=1:stop_threshold=-40dB output_tight.wav
```

`-ac 1` mono, `-ar` sample rate, `-ss` seconds of skip, `-af silenceremove=...` silence trimming. A handful of flags you'll reach for constantly.

## Which format, when?

- **Recording (capture):** Phone default (M4A/AAC) or WAV if the recorder insists. Don't agonize.
- **Transcribing (input):** WAV 16 kHz mono is safest because *every* local STT tool takes it natively; but Whisper tools happily take MP3/M4A directly. If the transcript looks weird, convert to WAV and retry — it removes a whole class of container weirdness.
- **Keeping as master/archive:** FLAC (lossless, ~50–60% of WAV size) if you care about the original waveform; otherwise keep MP3 64–128 kbps mono.
- **Sharing the transcript output:** plain `.txt` for input to tools, `.md` for people, `.srt`/`.vtt` when you want to sync to video later. All are bytes-cheap; generate every format while you're at it.

Bottom line: **one hour of any decent speech recording ≈ 30–115 MB, and the transcript of it ≈ 55 KB.** Budget with the [Workflow Sheet](workflow-sheet.html) and never be surprised by a "disk full" error at hour 3 of a recording again.
