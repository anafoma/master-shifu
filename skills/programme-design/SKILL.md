---
name: programme-design
description: >
  This skill should be used when the user asks to "design my programme", "make me a split",
  "build my routines", "plan my week", "redo my programme", "set up a new block", or wants
  workouts created in Hevy. It turns a confirmed training profile into a weekly split with
  sets per muscle, exercise selection and order, rep ranges and effort targets, and can
  create the routines in Hevy.
metadata:
  version: "0.1.0"
---

# Programme design

Build a programme from a confirmed profile. If no profile exists, run `intake` first.

## Steps

1. **Choose the split** from days per week (`references/intake.md`). Prefer each muscle trained at least twice weekly.
2. **Set weekly volume per muscle** (`references/training-science.md`):
   - Priority muscles: 12–20 sets/week (rank 1 highest).
   - Other muscles: 6–10.
   - Maintenance (if time is short): about 4.
   - Count indirect work as half a set (bench = 1 chest + 0.5 triceps + 0.5 front delt; presses also partly side delts).
   - Cap about 6–8 hard sets per muscle per session; add a day rather than more sets.
3. **Fit the session budget.** Working sets per session must fit session length (≈ 2.5–3 min per set + 10 min warm-up). If the total doesn't fit, cut sets from non-priority muscles first.
4. **Pick exercises** from `references/exercise-tiers.md`:
   - Prefer S/A tier, matched to equipment and the user's preferences and existing Hevy exercises (continuity helps progression tracking).
   - Use the "only 25 exercises" list as the default menu, and Nippard's own one-year upper and leg sessions (`references/workout-templates.md`) as proven starting templates.
   - Choose stretch-biased options deliberately for calves, hamstrings, quads and triceps; elsewhere prefer what the user feels and progresses on (`references/training-science.md`, "The stretch").
   - Program a warm-up: light cardio, then a ramp-up pyramid before the first heavy lift.
   - At least one isolation exercise for biceps, side delts, hamstrings and calves.
   - Never include an exercise the user said hurts or wants to avoid.
5. **Order within a session:** power work first (if any), then the top-priority muscle, heavy compounds, then isolation; failure sets last.
6. **Set reps and effort** by goal (`references/goals-strength-athletic.md`):
   - Hypertrophy, effort by type (`references/muscle-ladder.md`): heavy compounds RPE 6–8 (rising across sets), secondary compounds RPE 8–10, isolation RPE 9–10.
   - Rep mix across the week: ~60–80% of sets at 6–15 reps, 10–20% at 1–5, 10–20% at 15–30.
   - Strength lift: 3–6 reps at 1–3 RIR, more frequent practice.
   - Rest: isolation 1–2 min, light compounds 2–3 min, heavy compounds 3–5 min.
   - Vary exercises for the same muscle across the week (e.g. back squat Monday, hack squat Thursday).
   - Default split for 4 days is upper/lower, Nippard's favourite for size and strength.
   - Plan a 4–8-week build then a deload week (calculated: −30–50% sets, ~1–3 RPE easier).
7. **Progression rule** for every exercise: double progression within the rep range (see `progression`).
8. **Present the plan** as one compact table per day (exercise, sets × reps, RIR, rest), plus a weekly sets-per-muscle summary. Explain the 2–3 most important choices in plain words.
9. **Create in Hevy (on confirmation).** Follow `references/hevy.md`: create a folder named after the block (e.g. "Shifu Block 1, Nov 2026"), find template IDs with `search_hevy_exercises`, then create one routine per day with target sets, reps and starting weights from recent logs. Never overwrite the user's existing routines without asking; offer to archive them into a folder instead.

## Defaults when the user is in a deficit

Offer the lower-volume option (`references/training-science.md`, 100-day experiment): about 1–2 hard sets per exercise, ~6–10 sets per muscle weekly, high effort. Present it as an option with its evidence level.

## Quality checks before presenting

- Every priority muscle hits its weekly set target; nothing exceeds the per-session cap.
- Each day fits the session length.
- No avoided exercises; no D/F-tier picks unless the user insists.
- Starting weights come from real logs where available; otherwise say "pick a weight you can do for the top of the range at ~2 RIR".
