# The Workflow Sheet

One page. Print it, tape it near the recorder, stop re-deriving the pipeline from memory.

## BEFORE you press record (30 seconds)

- [ ] Soft room (carpet/curtains > glass/tile), fans/HVAC off or away
- [ ] Mic within arm's reach of the quietest important talker
- [ ] Phone/recorded test of one sentence, played back loud ✓
- [ ] Battery + storage for planned length + margin (rule of thumb: 64 kbps mono MP3 ≈ 0.5 MB/min; WAV 16 kHz mono ≈ 2 MB/min)
- [ ] Filename convention: `YYYY-MM-DD-what-where.mp3`
- [ ] Multi-speaker? Note who's present at the top of the recording; tap/say "next speaker" at each change

## TRANSCRIBE

- [ ] (Optional) Convert to 16 kHz mono, squeeze silences:
      ```bash
      ffmpeg -i in.m4a -ac 1 -ar 16000 -af silenceremove=stop_periods=-1:stop_duration=1:stop_threshold=-40dB out.wav
      ```
- [ ] whisper.cpp, `base` or `small` model, VTT output for timestamps:
      ```bash
      ./whisper-cli -m models/ggml-base.en.bin -f out.wav -ovtt --prompt "Speakers: <names>"
      ```
- [ ] Long silences trimmed beforehand (models invent speech hallucinations in silence)

## CLEAN UP (tier in brackets = minutes per hour of audio)

- [ ] **Names first:** list every name/term; find-and-replace with review, never blind
- [ ] **Chunks:** split the mega-paragraph by idea, 1–6 sentences each
- [ ] **Fillers:** delete "um/uh" and dry restarts — **never swap a word for a word** (keep "gonna", dialect, pet phrases — that's voice)
- [ ] **Trust check:** read the first + last 5 minutes; hunt hallucinations (fluency over silence, "Thanks for watching!")
- [ ] `T1` searchable ~5 / `T2` readable ~15–30 / `T3` publishable 60+; pick in advance

## LABEL SPEAKERS (one mic, multi-person)

- [ ] Play transcript at 1.5–2× using VTT timestamps + your "next speaker" taps
- [ ] Label format: `RAVI: ...` one line per turn
- [ ] Uncertain at 95%? Label `UNKNOWN (0:37:12)` and move on — never guess a person's name
- [ ] Everyone local-recorded on their own device? Label by file instead of by ear

## SUMMARIZE (all local, no keys)

- [ ] Ensure Ollama running: `curl http://localhost:11434/v1/models`
- [ ] Model: `llama3.2:3b` (default) / `llama3.1:8b` if 16 GB RAM
- [ ] Backed:
      ```bash
      python3 scripts/summarize_transcript.py meeting.txt            # Ollama default
      # repoint anywhere OpenAI-compatible:
      python3 scripts/summarize_transcript.py meeting.txt --base-url http://localhost:1234/v1 --model qwen2.5:7b
      ```
- [ ] Long transcript? Stage it: outline every 15 min → merge outline → targeted pulls quoting exact sentences → YOU write the final summary
- [ ] Context window: ask for ≥16k, or the script's default; a 1-hour transcript ≈ 12,000 tokens
- [ ] Action-item prompt ends in a checklist: WHO / WHAT / WHEN

## PRIVACY CHECKPOINT (one decision)

```
RECORDING/TRANSCRIBE/CLEAN/LABEL/SUMMARIZE ... all local by default
SHARE as text (summary, reviewed) → your deliberate choice; audio stays home
```
