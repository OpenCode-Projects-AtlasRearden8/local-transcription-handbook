# 1. Record Smart

The cheapest way to get a clean transcript is to start with clean audio. Speech-to-text models are remarkably good, but no model can recover syllables the microphone never captured. Five minutes of thought before you press record saves an hour of cleanup.

## The one rule: signal, then noise

A microphone only hears *difference*. A talker 5 meters away sounds like a whisper in a river of room echo. A talker 30 cm away sounds like a person. Nearly every "the transcript is garbage" problem traces back to distance from the mic.

**Move the mic closer before you touch any setting.** This beats software, beats settings, beats everything.

## Rooms: the invisible instrument

You're never just recording a voice — you're recording a room. Hard parallel surfaces (glass tables, bare walls, tile floors) reflect the voice back as echo, which smears consonants. Consonants are where speech-to-text lives or dies.

Quick room fixes, in order of impact:

1. **Pick a soft room.** Carpets, curtains, bookshelves, a car interior (parked — never while driving) are your friends. Empty conference rooms with glass walls are your enemy.
2. **Kill the hum sources.** Doors, HVAC, laptops with spinning fans, break rooms with dishwashers. Fan noise reads to the model as "someone said a short word just then," and Whisper *will* invent one.
3. **Mind the echo window.** In a hard rectangular room, sitting in the center beats sitting in a corner, where reflections pile up.

If you're stuck in a hard room: get the mic close (see the rule above) and put something soft between the talker and the nearest bare wall — a coat over a chairback genuinely helps.

## Phones: the recorder you already own

Your phone's built-in voice memo app is a genuinely good starting recorder. Three habits make phone recordings transcribable:

- **Hold the phone like a birthday cake.** Bottom edge (where the mics live) toward the speaker, under a meter away. Do not let your hand cover the mic hole — a muffled "PKW" where a name should be is the signature of a blocked mic.
- **Voice memos ≠ phone calls.** Call audio (Zoom, FaceTime, cell calls) is heavily compressed by voice-optimized codecs; it transcribes worse than the same mic recorded locally. On a call app, record *with the platform's own record button* using its supported layout, or better, record locally and merge later.
- **New recordings need one quiet test.** Record the first sentence, stop, play it back at full volume *through the phone speaker* before continuing. Catching a broken mic or a "recording the pocket" mistake costs 10 seconds; catching it an hour later costs everything.

Settings to leave alone: the phone's own noise reduction and "wind reduction" are fine for intelligibility, no need to fight them. Record mono, record in the default format (AAC/M4A on iPhone and most Androids). One megabyte per minute is a typical phone figure — the [size math chapter](03-file-formats-size-math.html) explains why that's plenty.

## Pocket recorders: small, dumb, and dependable

Handheld voice recorders (ZOOM H1n and friends, plus the cheaper "recorder pen" class) are excellent because they do one job. What matters when you buy or use one:

- **Set the format once and leave it.** MP3 at 128 kbps, or WAV at 16-bit / 44.1 kHz or 16 kHz if the device has that rate. Both are fine for speech; WAV costs a lot more space for marginal gain. Flip to [file formats](03-file-formats-size-math.html) for the full math.
- **Beware recorders with "scene modes."** A "meeting" preset is real (it biases the mic pattern), but a "lecture at 20 meters" preset cannot conjure signal from that distance. The rule still applies: distance is physics.
- **Batteries and cards.** Fresh batteries for anything over an hour, and know where the file goes. A recording that lives on a microSD card in a drawer is a recording you don't have.
- **For a single speaker at a desk**, clamping it (or a lavalier mic) to a shirt pocket beats placing it on the table — table pickup gets thumps, tapping, and reflection-bounce off the wood.

A $40 recorder plus a $15 lapel mic will outperform a $300 recorder left on the far side of a table. Spend on proximity before you spend on price.

## Group recordings: the honest version

With one mic and four people, your choices are:

1. **Put the mic near one person** (usually you, taking notes as they talk), and note in the recording who else is speaking. See the [speaker-labeling chapter](05-speaker-labeling.html) for turning that into a two-voice transcript.
2. **Put the mic in the middle and accept a messy transcript.** It'll transcribe — group discussions at one mic tend to arrive as a wall of run-together sentences. Readable after cleanup, but with gaps where two people overlapped.
3. **Ask everyone to record locally on their own device**, then stitch the tracks. More work, best result. Worth it for a board meeting or a class lecture with visiting speakers, overkill for a five-person yarning.

## The pre-flight checklist

Printable at [Workflow Sheet](workflow-sheet.html). The 30-second version:

- [ ] Best soft room available? Fan, dishwasher, door, printing room off?
- [ ] Mic within arm's reach of the *quietest* important talker?
- [ ] Test recording of one sentence, played back loud?
- [ ] Battery/space for the full planned length (with margin)?
- [ ] Filename convention ready, e.g. `2026-11-01-ct-meeting.mp3`? (You'll thank yourself.)
- [ ] If others are recording: are we on the same page?

## Real recording samples, worth a dollar

If you want calibrated ears, capture 30 seconds from each of your usual rooms — a good one and a bad one — and transcribe both with the same Whisper model. The transcript from the soft room with the close mic will be nearly flawless; the transcript from the hard room will be visibly worse, with the errors concentrated exactly where you stood far from the mic. That one experiment permanently recalibrates your recording instinct.

That's it. The rest of the book is about what happens to good recordings anyway. Onward to [the tooling](02-local-stt-options.html).
