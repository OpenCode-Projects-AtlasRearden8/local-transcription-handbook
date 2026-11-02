# 4. Cleanup Rules That Keep the Speaker's Voice

A raw Whisper transcript is accurate in words and wrong in *feel*: no paragraph breaks, mid-sentence stumbles reproduced verbatim, punctuation invented by a model that never heard a human being. The cleanup pass is where a transcript becomes readable.

The whole chapter comes down to one question: **are you transcribing what people said, or what you wish they'd said?** Both are legitimate, but they're different products, and mixing them up is how you lose a reader's trust.

## Two products: verbatim vs. clean verbatim

| | Verbatim (court-reporter style) | Clean verbatim (this book's default) |
| --- | --- | --- |
| Purpose | Legal, ethnographic, "quote them exactly" | Reading, sharing, summarizing |
| Filler ("um," "uh," "like") | Keep all | Remove fillers |
| Repeats & self-corrections ("I went— I went to—") | Keep | Remove, or keep if emphasis |
| False starts ("we were supposed to—" ) | Keep | Trim trailing, keep the restart |
| Word swaps | Never | Never — *see the hard rule below* |
| Punctuation | Add minimally | Fix fully |
| Paragraphing | Minimal | Frequent, by idea |

**The hard rule, unbreakable in either mode:** never swap a word for a word. You may delete a filler; you may not turn "kinda" into "kind of," or "gonna" into "going to." The first is cleanup; the second is ghostwriting. If a sentence is only understandable with your edit, put the meaning in brackets, not in the quoted sentence: `[referring to the new badge policy]`.

## The Whisper-shaped problems (and their fixes)

1. **A wall of text.** Whisper gives you one mega-paragraph. Fix: split paragraphs *by idea* — every time the topic changes or a new speaker starts a stretch of talking. A good paragraph in a transcript is 1–6 sentences; nobody is grading you on the grammar of paragraph breaks.
2. **Invented punctuation.** Whisper adds periods confidently and puts commas wherever it likes. Fix: re-punctuate by reading aloud; the "voice" of your punctuation should follow the speaker's own rhythm.
3. **Hallucinated phrases over silence.** A recurring classic: the transcript says something *nobody said*, usually fluent boilerplate ("Thanks for watching!") — the model filled a gap of silence/muzak/template audio. Fix: trim silences before transcribing (the `silenceremove` ffmpeg trick in [chapter 3](03-file-formats-size-math.html)); never publish a quoted sentence you don't remember hearing.
4. **Butchered names.** Whisper is brilliant at ordinary vocabulary and terrible at "Asdale," "ffxiv tank," "LaTisha." Fix: pre-empt with `--prompt "Speakers: LaTisha, Dylan Asdale"` where the tool supports it ([chapter 2](02-local-stt-options.html)); globally find-and-replace by ear afterward; when you can't identify the name, mark it `[unknown name]` rather than guessing.
5. **Numbers and dates.** "twenty twenty-five" vs "2025." Fix as speaker-intended: a date said as "twenty twenty-five" gets written as 2025; but an exact quoted rule like "twenty percent" stays if in doubt, write what the person meant, not whatever the model chose.

## The 10-minute cleanup pass (by hand)

A systematic order beats a fiddly read-through:

1. **First read for names.** List all names/technical terms; fix globally (find-and-replace, one at a time with *review* — never blind "replace-all," or you'll "fix" a benign match).
2. **Second pass for speakers.** Every time the speaker changes, do the labeling (full method in [chapter 5](05-speaker-labeling.html)).
3. **Third pass for paragraphs.** Split, split, split. Rest your eyes; a wall paragraph is a wall paragraph.
4. **Fourth pass: fillers and stumbles**, per your [verbatim-vs-clean table](#two-products-verbatim-vs-clean-verbatim). Read the passage *aloud in your head* with the deletion first; if meaning is lost, put it back.
5. **Final pass: the trust check.** Read the first and last 5 minutes only, hunting for hallucinations and punctuation defaults. Long-transcript trust is front-loaded; that's where readers look for quality signals.

## Keeping the voice while deleting the noise

This is craft, not mechanics. Heuristics that preserve a person's voice:

- **Keep idiosyncrasies that are *style*.** "Wanna," "gotta," "y'know ما" — personal diction is the fingerprint of a human. Fillers (um/uh) are the temporary scaffolding of speech, and removing them helps the sentence land; but permanent phrases are *identity*, not noise, and cutting them whitens everyone's voice into the same voice.
- **Keep laughter where it happens**: spelled out ("[laughs]") not interpreted ("jokingly"). Never interpret; always report.
- **Keep restarts when the restart IS the sentence.** "I— I no I don't want— I don't want the smallest one, I want the medium one" is a person correcting themselves in real time, and the stumbles carry the emotion. Trim the *dry vertical* re-restarts ("I went— I went to school") but keep *meaningful* ones.
- **One rule if ambiguities multiply:** if you have to *decide* what the person meant, that's a judgment call — use brackets and note it, or don't publish the quote at all. An honest `[inaudible 23:14]` beats a confidently wrong word.
- **When an LLM does the cleanup** (chapter 6 can help here): the model must be given the same hard rule — see the prompt in the [summarizer chapter](06-transcript-to-summary.html), which includes the verbatim-protection clause in bold. LLM cleanup drifts toward "make sentences nicer," which silently means "make sentences standard," which is *exactly* the voice erasure this chapter exists to prevent.

## The 3-tier cleanup ladder

Not every transcript deserves an hour. Pick the tier in advance and move on:

- **Tier 1 — searchable (5 min per hr of audio):** Light spell fixes of names, some paragraph breaks. For your own reference/archive.
- **Tier 2 — readable (15–30 min per hr):** Full [10-minute pass](#the-10-minute-cleanup-pass-by-hand), including speakers labeled. For sharing with the recorded group. **This is the right tier for 90% of recordings.**
- **Tier 3 — publishable (60+ min per hr):** Rounds of passes, checked quotes, a self-consistency pass, and a trust check. For books, journalism, content that will outlive the reader forgetfulness. Get the speaker to confirm direct quotes; your [recordings from chapter 1 workaround notes](01-record-smart.html) for hard rooms make this less necessary but never automatic.

Next, the fiddliest part mentioned above done properly: [Hand-Labeling Speakers](05-speaker-labeling.html).
