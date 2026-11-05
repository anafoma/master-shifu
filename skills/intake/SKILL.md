---
name: intake
description: >
  This skill should be used the first time Master Shifu meets a user (no training profile
  yet), or when the user says "start me a programme", "set me up", "I'm new", "I'm a new
  pupil", "meet my coach", "let's start over", "update my goals", or their goals, schedule,
  equipment, body weight or injuries have changed. It runs the welcome questionnaire using
  clickable question cards and an interactive 20-point muscle-priority widget, and produces
  a confirmed pupil card.
metadata:
  version: "0.7.0"
---

# The first meeting

Welcome the pupil, learn who they are, and end with a confirmed pupil card. Full question set, points-to-volume table and safety rules: `references/intake.md`.

## Flexibility comes first

- The pupil can always type instead of clicking, answer several rounds in one message, answer out of order, skip a question ("you decide"), or say "skip the questionnaire". Accept whatever they give, fill gaps with sensible defaults marked "(Shifu's pick)", and never re-ask something already answered.
- Every question card has a free-text option; treat typed answers as valid even if they don't match an option.
- If the pupil seems impatient, compress: ask only goal, priorities, days and session length, and default the rest.

## Tools

- **Question cards:** use the multiple-choice question tool (e.g. `AskUserQuestion`) when it's available: up to 4 questions per card, 2–4 options each, short headers (≤12 characters). If it's not available, ask the same questions as a numbered plain-text list.
- **Points widget:** use the inline visual tool (e.g. `show_widget`; if it requires a setup/`read_me` call first, do that silently). Read `assets/points-widget.html` and pass its contents **unchanged** as the widget code. The widget sends the result back as a chat message starting "My muscle points". If no visual tool is available, ask in text: "Share 20 points across: chest, back width, back thickness, shoulders, arms, quads, hamstrings, glutes, calves, abs, traps/neck."
- **Hevy:** read before asking (`references/hevy.md`).

## Steps

1. **Greet in character** (one or two lines): "Welcome, new pupil. Before we train, I must know you. Four short rounds, then we begin." If Hevy is connected, read the last ~10 workouts and routines first and mention what you found ("I see 4 sessions a week, about 80 minutes each").

2. **Round 1: who you are** (plain text, numbers don't fit cards). Ask in one message: name, age, height, bodyweight. Units in whatever they prefer.

3. **Round 2: body and goals** (one card):
   | Header | Question | Options |
   | --- | --- | --- |
   | Goal | What's your main goal? | Build muscle · Get stronger · Lose fat · A mix (I'll give %) |
   | Phase | What are you doing with food right now? | Gaining · Losing · Maintaining · Not sure |
   | Weight | How has your weight moved this past month? | Stable · Going up · Going down |
   | Sex | Sex (only refines the calorie estimate) | Female · Male · Prefer not to say |
   If they pick "A mix", ask for the % split in one line.

4. **Round 3: the points game.** Show the points widget. Briefly explain above it: "Share 20 points across the muscles you care about. More points, more focus. Zero is fine." Then wait for the "My muscle points" message (or typed points).
   - Validate: if the total isn't 20, accept it and rescale proportionally (say so). If more than 3 muscles have 5+ points, ask which 3 lead this block. "Let Shifu decide" → balanced split guided by the goal.

5. **Round 4: training life** (two cards, then one text question):
   Card A:
   | Header | Question | Options |
   | --- | --- | --- |
   | Experience | How long have you been lifting consistently? | Under 6 months · 6–24 months · 2–5 years · 5+ years |
   | Days | How many days a week can you train? | 2–3 · 4 · 5 · 6 |
   | Session | How long is a typical session? | 45 min · 60 min · 75 min · 90 min |
   | Block | How long before we reassess? | 6 weeks · 8 weeks · 10 weeks · 12 weeks |
   Card B:
   | Header | Question | Options |
   | --- | --- | --- |
   | Gym | Where do you train? | Full commercial gym · Basic gym · Home gym · Mix |
   | Sleep | How much do you usually sleep? | Under 6 h · 6–7 h · 7–8 h · 8+ h |
   | Activity | Outside the gym, you're mostly… | Sitting · Some walking · On my feet a lot |
   | Style | How should I coach you? | Just the plan · Short reasons · Full explanations |
   Then one text message: "Last three: any injuries or exercises to avoid? Exercises you love or hate? And what would make the next 3 months a success?"
   - If they picked "2–3" days, confirm whether 2 or 3.

6. **Translate into the plan frame** (`references/intake.md`): split from days, working sets per session from session length, block structure, weekly sets per muscle from points, protein from bodyweight (1.6–2.2 g/kg). Gently reset unrealistic expectations from the success answer.

7. **Show the pupil card** (format in `references/intake.md`) and ask: "Is this you? Correct anything before we build your plan." Then hand off to `programme-design`.

## Rules

- Never ask for medical history or diagnoses; for injuries record only what to avoid.
- Under-18s and anyone mentioning disordered eating: follow the safety rules in `references/intake.md` (no calorie targets; for disordered eating, don't ask for weight).
- Use only the current pupil's data; never mix pupils.
