# 2. Free Local Speech-to-Text, Compared

There is no one best free transcriber. There is a best transcriber *for your situation*: your machine, your languages, your patience for setup, and how much punctuation you want to do by hand. Here's the honest map.

## The contenders at a glance

| Tool | Accuracy (English) | Punctuation out of the box | Speed on old laptop | Speed w/ GPU or Apple Silicon | Setup difficulty | Languages |
| --- | --- | --- | --- | --- | --- | --- |
| **whisper.cpp** (`base`) | Very good | Yes | Minutes per hour of audio | Seconds–minutes | Easy (one binary) | ~100 (be honest: ~99 usable) |
| **faster-whisper** (Python) | Very good (same models) | Yes | Minutes | Very fast | Moderate (Python + pip) | ~100 |
| **OpenAI Whisper** (original Python) | Very good | Yes | Slower than both others on CPU | Same models, same speed rules | Moderate | ~100 |
| **Vosk** | Good, noticeably below Whisper | **None** | Fast even on CPU-only tiny machines | Fast | Easy (pip, small models) | 20+ |
| **speech_recognition + pocketsphinx** | Poor-to-mediocre | None | Very fast | Same | Easy | Few |
| **Online free tiers** (not local) | Excellent | Yes | n/a | n/a | Easy | Many |

Notes on the honest parts people skip:

- **The three Whisper variants read the same model file and produce near-identical text.** Choose on *convenience*: whisper.cpp if you like one binary and a terminal; faster-whisper if you live in Python and want the fastest CPU/GPU inference; the original OpenAI Whisper if a tutorial you're following uses it. Accuracy differences between them are smaller than the difference between model sizes.
- **Model size is the real accuracy dial.** `tiny` is fine for notes, `base`/`small` is the everyday sweet spot, `medium`/`large` breathe on faster hardware. See the table in [the size chapter](03-file-formats-size-math.html) for what each model costs you in RAM and time.
- **Vosk's lack of punctuation is a feature and a dealbreaker.** It's genuinely fast and small (runs on a Raspberry Pi), but every transcript comes out as a lowercase river. If your workflow ends at "readable text," that's a lot of manual work; if your workflow feeds an LLM summarizer (chapter 6), it can cope — but Whisper usually still wins on accuracy for the same machine.
- **Hallucination on silence.** All Whisper variants occasionally invent fluent nonsense over long pauses, door slam? music, or very short clips — *the model has learned that audio usually contains speech, so it writes some.* The practical fix: trim long silences before transcribing (ffmpeg `-af silenceremove`), or keep chunks under ~1 minute. This is listed again in the [cleanup chapter](04-cleanup-rules.html) because it's the #1 "but the transcript says something nobody said!" mystery.
- **Pocketsphinx and friends are history's gifts.** Still useful for tiny offline embedded setups, and a useful *floor* to compare against when you want to feel how good the modern options are. Not the right daily driver for book-quality transcripts.

## Choosing in three questions

1. **Do you want one command in a terminal, or are you comfortable with Python?**
   One command → **whisper.cpp**. Python-native → **faster-whisper**.
2. **Do you need punctuation and paragraphing basically done for you?**
   Yes → Whisper-family. No, and you'll pay per CPU-cycle dearly → Vosk.
3. **Are you transcribing mostly English?**
   English → `base` or `small` Whisper models are superb. Another language → check the [Whisper language support list](https://github.com/ggml-org/whisper.cpp#supported-language); use the larger models (`medium`+) where your language lives at lower accuracy.

## A whisper.cpp starter (the one-liner path)

Install per the [whisper.cpp GitHub page](https://github.com/ggml-org/whisper.cpp) (a binary is packaged for the usual platforms), download a model, and:

```bash
./whisper-cli -m models/ggml-base.en.bin -f meeting.wav -otxt
# text appears as meeting.txt
```

That's genuinely the whole pipeline for the common case. Options you'll actually use:

- `-otxt` / `-osrt` / `-ovtt` — text, subtitles, or timestamped VTT output.
- `-t 4` — CPU threads; try your core count and leave it.
- `--prompt` — give the model a nudge about topic or unusual spellings ("names: Dylan Asdale") to cut mis-heard names.
- `-l en` for English-only models (`.en` weights, faster and more accurate on English).

Everything in this chapter is measured in honest terms: the *model* matters more than the tool, the *recording* matters more than the model, and the *cleanup pass* (chapter 4) matters more than any of the above. The world-class model transcribing a bad recording produces a bad transcript with perfect punctuation.

Onward: what those WAV files actually weigh → [File Formats and the Size Math](03-file-formats-size-math.html).
