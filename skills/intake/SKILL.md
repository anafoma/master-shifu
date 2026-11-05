---
name: intake
description: >
  This skill should be used when the user wants a new training programme, says "start me
  a programme", "set me up", "I'm new to the gym", "build me a plan" and no training profile
  exists yet, or when their goals, schedule, equipment or injuries have changed. It gathers
  the nine intake answers and produces a confirmed training profile.
metadata:
  version: "0.1.0"
---

# Intake

Gather what programme design needs, with as few questions as possible.

## Steps

1. **Check what's already known.** Look in the conversation and any saved context for an existing profile. If Hevy is connected, read the last ~10 workouts and the routines (`references/hevy.md`) to infer days per week, session length, current loads, split and favourite exercises.
2. **Ask only what's missing** from the nine questions in `references/intake.md`. Ask at most 3–4 at a time; use multiple-choice questions where the interface supports them. Order: goal, priority muscles, days per week, session length, programme length, then the rest.
3. **Turn answers into constraints** using the tables in `references/intake.md`: split from days per week, working-set budget from session length, block length from programme length.
4. **Play back the profile** as a compact block and ask the user to confirm or correct it:

```
Goal: hypertrophy 80 / strength 20
Priorities: 1 hamstrings, 2 glutes, 3 shoulders
Schedule: 4 days, ~75 min (≈ 20 working sets per session)
Block: 8 weeks, reassess at week 8
Level: intermediate (3+ yrs); current: hip thrust 100 kg × 12
Equipment: full commercial gym
Avoid: none
Phase: maintaining
```

5. **Hand off** to `programme-design` once confirmed.

## Rules

- Never ask for medical history. If the user mentions an injury, record only what to avoid ("no overhead pressing, shoulder"), not diagnoses.
- If the user says "you decide", choose sensible defaults, state them in the profile, and proceed.
- Priority muscles are ranked: order matters for volume and exercise order later.
