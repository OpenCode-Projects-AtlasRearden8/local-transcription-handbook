# 7. What Stays Offline

"Local-first" isn't a religion; it's a security decision you make *on purpose, per step*. This chapter is the shortest one on purpose, because the answer is the same for almost every step of this handbook.

## The default policy

| Step of the workflow | Where it runs | Default |
| --- | --- | --- |
| Recording (phone/recorder) | On-device | **Offline always** |
| Transcription (Whisper/Vosk) | Your machine | **Offline always** |
| Cleanup (chapter 4) | Text editor on your machine | **Offline always** |
| Speaker labeling (chapter 5) | Text editor + player, on your machine | **Offline always** |
| Summarization (chapter 6) | Ollama or any local endpoint | **Offline by default** |
| Publishing/sharing the *transcript* | Wherever you choose | Your call, after a read-through |
| Publishing/sharing the *summary* | Wherever you choose | Your call — the summary is the only thing worth an extra look |

**Audio and raw transcripts of real conversations are the most private data in this whole handbook** — more private than your documents, arguably as private as your messages. People say things into a mic on the understanding that they *said it*, not that they *published it*. The whole point of doing everything locally is that the sensitive stuff never crosses an internet boundary you didn't choose.

## Why all local is practical, not just principled

Chapter by chapter, the local option isn't a compromise anymore:

- **Transcription:** Whisper `base` runs offline on a laptop and is better than most cloud APIs of two years ago. The gap that remains to the best cloud models is small and shrinking, and irrelevant for meetings and notes.
- **Summarization:** a local 3B model summarizing a chunked transcript is *good*, and the failure modes (chapter 6's table) are things you check for in 30 seconds.
- **No accounts, no keys, no data-retention fine print, no "we improved our models using your content" toggle to find.** The entire privacy policy of your pipeline is one sentence: *it never left.*

## The honest exceptions

Saying "never online" would just be wrong. Here's where online earns its keep — each one a decision you make, not a default:

1. **Accuracy-critical verbatim on hard audio** (noisy legal deposition, fragile dialects). Cloud STT is still ahead on the nastiest input. Decision rule: *is the difference in accuracy worth this recording existing on someone else's server?* For a memoir transcript of Grandpa's stories, do NOT upload them; retry locally with a bigger model instead.
2. **Quota/limits genuinely block you** — a 10-hour overnight dictation with a small laptop. Chunking + a bigger local model ([chapter 6](06-transcript-to-summary.html)) may honestly be easier than uploading. YMMV — but this one is an honest "maybe."
3. **Collaborative editing of a summary** you want in Google Docs *anyway* — fine. Only the *finished, reviewed* text goes there; no audio, no raw raw-transcript, and (per chapter 4) no verbatim quotes of what sensitive speakers said that you haven't reviewed for publication-worthiness.

And a special case that trips people up: **the video/web meeting platform.** Zoom or Meet is *inherently* a cloud service; local recording within it keeps bytes on your machine but the meeting's audio may still transit the platform's servers. If the content is sensitive choice: meet on a locally-hosted option, or accept the recorded-content policy of the platform while keeping *this handbook's outputs* (transcript + summary) on your machine.

## A "does this need the internet?" free-flow table you can build in 20 seconds

If you keep any habit from this chapter, keep this table in your notes file for the project at hand:

```
RECORDING     : offline (phone/recorder)          ✔ private
TRANSCRIBE    : whisper.cpp base                  ✔ private
CLEAN/LABEL   : text editor                       ✔ private
SUMMARIZE     : Ollama localhost:11434            ✔ private
FINAL SUMMARY : maybe Google Docs to share        ◯ my choice, reviewed
```

Five lines; the *private* cases are visible at a glance, and the one choice you made is explicit rather than ambient.

## The sentence to keep

**Everything before "publish" happens on your machine by default. What goes online is a deliberate decision, made for a finished and reviewed product, and shared *as text* — the audio stays home.**

That closes the loop of the handbook: [Record Smart](01-record-smart.html) → [Pick a tool](02-local-stt-options.html) → [Do the math](03-file-formats-size-math.html) → [Clean it](04-cleanup-rules.html) → [Label it](05-speaker-labeling.html) → [Summarize it](06-transcript-to-summary.html) → [Keep it private](#what-stays-offline). The [Workflow Sheet](workflow-sheet.html) puts the whole loop on one page you can print.
