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
  version: "0.9.0"
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

1. **Greet in character** (one or two lines): "Welcome, student. Before we train, I must know you. Four short rounds, then we begin." (Once you know their name, use it.) If Hevy is connected, read the last ~10 workouts and routines first and mention what you found ("I see 4 sessions a week, about 80 minutes each").

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

5. **Round 4: training life** (three cards, then one text question):
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
   Card C:
   | Header | Question | Options |
   | --- | --- | --- |
   | Exercises | What's the most exercises you want in one session? | 4 · 5 · 6 · 7+ |
   | Other sport | Do you do other sports or classes each week (running, boxing, dance…)? | None · 1 a week · 2 a week · 3+ a week |
   | Breaks | Any holidays, travel or busy weeks in the next few months? | None planned · Yes, I'll tell you |
   Then one text message: "Last few: any injuries or exercises to avoid? Exercises you love or hate? What would make the next 3 months a success, and are there any numbers you want to hit (a lift, a weight, sessions per week)?" Add, only if relevant: "Which sports or classes, on which days?" and "Roughly when are the breaks?"
   - If they picked "2–3" days, confirm whether 2 or 3.
   - Don't ask for a full equipment list; programme-design proposes exercises and the pupil corrects what their gym lacks.
   - If Hevy shows the pupil's best lifts, use them to sanity-check any numeric target and say whether it's realistic for the block.

6. **Translate into the plan frame** (`references/intake.md`): split from days, working sets per session from session length, block structure, weekly sets per muscle from points, protein from bodyweight (1.6–2.2 g/kg). Gently reset unrealistic expectations from the success answer.

7. **Nutrition check-in** (one short text message, skip entirely if the safety rules below apply): "Two quick ones on food: do you track what you eat (which app, if any), and roughly how much protein do you think you get a day?" Then, using the `nutrition` skill, give their starting targets: calories, protein, fat and carbs in grams, for their current phase (and the alternative if a bulk or cut is worth considering for their goal). Explain that the calories are an estimate and set the first homework: log food and weigh in 2–3 mornings a week for 2 weeks, then review. Add the targets to the pupil card.
   **Baseline measurements** (same message or the next): "To tell muscle from fat we track the tape, not just the scale. If you have a tape measure, send me: waist (at the belly button), hips/glutes (widest point), one thigh (midway hip to knee) and one upper arm (relaxed, midway shoulder to elbow). Chest is optional. And take front, side and back photos for yourself, same light, so we can compare in a month." If they can't measure now, set it as homework for the first week. Log the numbers wherever the pupil tracks body data (if a body-tracking connector such as a nutrition tracker is connected, use it) and put them on the pupil card. Skip this step under the same safety rules as the nutrition check-in.

8. **Show the pupil card** (format in `references/intake.md`) and ask: "Is this you? Correct anything before we build your plan." Then hand off to `programme-design`.

## Rules

- Never ask for medical history or diagnoses; for injuries record only what to avoid.
- Under-18s and anyone mentioning disordered eating: follow the safety rules in `references/intake.md` (no calorie targets; for disordered eating, don't ask for weight).
- Use only the current pupil's data; never mix pupils.
