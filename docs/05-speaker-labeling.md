# 5. Hand-Labeling Speakers

You recorded a conversation with one mic. Whisper transcribed it faithfully — as one continuous monologue by one invisible ghost. Now: *who said what?*

## The honest state of speaker identification

There exist real automatic tools for this ("diarization"). Free options like `pyannote-audio` exist and work — sometimes well. Here's the honest picture:

1. **They work best with two clear voices, one mic, no overlap.** That's also the case you'd handle fine by hand.
2. **They add real setup weight** (Python dependencies, model downloads, HF account gating).
3. **They still mislabel** ≈ a significant fraction of turns in real-world rooms — noisy backgrounds, similar voices, the machine will confidently tell you the story is "A, B, A, A, B" when it was "A, B, B."

For a single recording you're already editing by hand ([chapter 4](04-cleanup-rules.html)), labeling by hand is usually *faster overall* and more trustworthy. Diarization earns its keep in bulk (100 recordings, same setup each time) — not in your five-person meeting.

## Setup that makes hand-labeling fast

The work happens at two moments — one before recording, one after — each worth ten seconds of habit.

**At recording time (from [chapter 1](01-record-smart.html)):**

- Capture timestamps mentally: every time the speaker changes ("new speaker"), tap the recorder, say "next speaker," or note the phone-clock time (e.g., "3:12, Priya starts"). Two seconds per speaker change beats arriving home to a mystery.
- If two people's speaking turns already flow in a predictable rhythm, audibly note turn order at the top: "This is Priya, then me, alternating."

**Right after transcribing:**

1. Open the transcript with timestamps visible. Whisper's `-otxt` text strip timestamps; use `-ovtt`/`-osrt` output (or `--output_format vtt`) so you see a timestamp every few lines, cheaply. The [size chapter](03-file-formats-size-math.html) has the flags.
2. Play the audio alongside at **1.5×–2× speed**. You're not relistening content, you're triaging *voice identity*.

## The labeling pass, step by step

Work with two identifying properties of each voice — *timbre* (male/female/child/high/low/gravelly) and *pattern* (the person who says "[…] actually" or "hm hm"). Then:

1. **Mark the first unambiguous lines.** Using the speaker change markers from recording time, label a handful of certain moments at the top of the file ("Ravi" at 00:12, "me" at 00:48). Don't label everything yet.
2. **Scrub every section change, guided by your recorded cues.** "Next speaker" (you tap/whistle) is your map. Between cues, verify the new voice by timbre and pattern.
3. **Label with a consistent edit pattern you can automate** — for instance a one-line tag before each turn:
   ```
   RAVI: So the Zettelkasten idea is higher value per unit of thought.
   DYLAN: Mm. Walk me through the filing part.
   ```
   Plain text survives anything (find-and-replace them later for polish — the [size chapter](03-file-formats-size-math.html) recommends a simpler ASCII form for that: `RAVI:` with no spaces is faster to search).
4. **Ambiguity policy, decided in advance:** If you can't label with confident 95% correctness, label as `UNKNOWN (00:37:41)` and move on — with the timestamp so a relisten later is easy. Never guess a name for attribution to a real person. This matters the most when a transcript will be seen by a third party.
5. **One voice or two?** Use the narrator trick: read a suspicious passage aloud, voice-acted, in the two candidate voices. Your ear knows voices — the reading is just how you get from brain to microphone to consciousness.

## When several mics or remote callers join in

- **Everyone records themselves on the phone** ([chapter 1](01-record-smart.html)). Then per-speaker mono WAV, all at 16 kHz — label by file, not by ear: `speaker= priya.wav` is labeling with zero effort.
- **Zoom/Meet local multi-track recordings.** The platform *saves each participant as a separate track* when the host clicks "record locally," and the export gives you one audio file per participant. Label by file, not by ear — that beats any hand-labeling. (Online hosts, see [what stays offline](07-what-stays-offline.html) for the privacy trade.)
- **One mp3 with multilingual speech segments.** Whisper's `-ml` flag (or segment-confidence scores with faster-whisper) can hint at language shifts; a language switch is often a speaker switch, too. Used sparingly, this is a decent scrubbing hint.

## Sizing your expectations

One hour of a four-person meeting ≈ 60 speaker turns ≈ **20–30 minutes of careful labeling and verification** with the method above. That time is the price of being *correct*; diarization partly buys you a different and worse price — you'll spend 15 minutes in setup on every future meeting and you'll get 3 mislabels of "A, B, B, A" to manually fix anyway.

For the fraction of recordings where every line of *who* matters (interviews, board minutes, research), it's a fair trade.

Next: the transcript is clean and labeled. Now the door opens for the LLM summarizer — [From Transcript to Summary](06-transcript-to-summary.html).
