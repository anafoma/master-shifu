---
name: programme-design
description: >
  This skill should be used when the user asks to "design my programme", "make me a split",
  "build my routines", "plan my week", "redo my programme", "set up a new block", or wants
  workouts created in Hevy. It turns a confirmed training profile into a weekly split with
  sets per muscle, exercise selection and order, rep ranges and effort targets, and can
  create the routines in Hevy.
metadata:
  version: "0.11.0"
---

# Programme design

Build a programme from a confirmed profile. If no profile exists, run `intake` first.

## Steps

1. **Choose the split** from days per week (`references/intake.md`). Prefer each muscle trained at least twice weekly.
2. **Set weekly volume per muscle** (`references/training-science.md`):
   - Use the pupil's muscle points (`references/intake.md`, points table): 5+ points → 16–20 sets (hamstrings ~12–15), 3–4 → 12–16, 1–2 → 8–12, 0 → 4–8.
   - If there are no points yet, ranked priorities: 12–20 sets for priorities, 8–12 for the rest.
   - Count indirect work as half a set (bench = 1 chest + 0.5 triceps + 0.5 front delt; presses also partly side delts).
   - Cap about 6–8 hard sets per muscle per session; add a day rather than more sets.
   - **Count with the calculator, not by hand:** `scripts/shifu_calc.py sets` with each exercise's sets, `primary` and `secondary` muscles, and the Shifu targets. It returns direct, Nippard and fractional counts, status and gap per muscle, and flags any muscle over 8 direct sets in one session.
   - **Do the budget arithmetic up front.** Weekly set budget = days × sets per session (step 3). Add up the targets for every muscle. If the targets exceed the budget (they usually do: 11 muscle groups × 10 sets is 110+ sets a week), say so plainly before presenting and explain that the points decide who gets growth volume and who gets maintenance. A gap on a low-point muscle is then a trade-off, not a surprise.
3. **Fit the session budget, using the pupil's real pace.**
   - **Pace from logs:** from the last ~10 Hevy sessions, minutes per set = session duration ÷ sets logged (skip sessions marked "forgot to stop"). Most people land at 4–4.5 min per set once warm-ups, walking between machines and set-up are included. No history → assume 4 min per set. Never assume 2.5–3 min.
   - Run `scripts/shifu_calc.py budget` with the raw Hevy workouts, the session length, the exercise cap and each day's planned sets/exercises: it returns the median pace (skipping implausible sessions), how many sets fit, and each day's expected minutes and cap check.
   - Working sets per session = session length ÷ pace, and say the expected duration per day when presenting.
   - **Exercise cap:** respect the pupil's max exercises per session (from intake; default 5–6). It's separate from the set count: 18 sets over 5 exercises feels fine, 7 exercises feels endless. When a day goes over, cut the exercise that serves the lowest-point muscle and move a set to a remaining exercise that covers it partly (e.g. drop a lat pulldown, add a set to a row).
   - If the total doesn't fit, cut sets from non-priority muscles first.
4. **Pick exercises** from `references/exercise-tiers.md`:
   - **S/A tier by default.** Anything lower needs a stated reason (e.g. a barbell hip thrust kept because it's the pupil's goal lift) or the pupil's explicit preference.
   - Match the pupil's preferences and existing Hevy exercises (continuity helps progression tracking).
   - **Equipment: propose, then let the pupil correct.** Pupils won't list every machine. Pick from what a gym of their type normally has, and keep a same-tier fallback ready for each pick (e.g. preacher curl → Bayesian cable curl) so a "we don't have that" is a quick swap.
   - **Cues from the knowledge, not memory.** Technique cues in the plan and in Hevy notes must match the technique notes in `references/exercise-tiers.md` (e.g. hip abduction: sit tall, hips extended).
   - Use the "only 25 exercises" list as the default menu, and Nippard's own one-year upper and leg sessions (`references/workout-templates.md`) as proven starting templates.
   - Choose stretch-biased options deliberately for calves, hamstrings, quads and triceps; elsewhere prefer what the user feels and progresses on (`references/training-science.md`, "The stretch").
   - Program a warm-up: light cardio, then a ramp-up pyramid before the first heavy lift.
   - At least one isolation exercise for biceps, side delts, hamstrings and calves.
   - Never include an exercise the user said hurts or wants to avoid.
5. **Order within a session:** power work first (if any), then the top-priority muscle, heavy compounds, then isolation; failure sets last.
6. **Set reps and effort** by goal (`references/goals-strength-athletic.md`):
   - Hypertrophy, effort by type (`references/muscle-ladder.md`): heavy compounds RPE 6–8 (rising across sets), secondary compounds RPE 8–10, isolation RPE 9–10.
   - Rep mix across the week: ~60–80% of sets at 6–15 reps, 10–20% at 1–5, 10–20% at 15–30.
   - Strength lift: 3–6 reps at RPE 7–9 (1–3 reps left), more frequent practice.
   - Rest: isolation 1–2 min, light compounds 2–3 min, heavy compounds 3–5 min.
   - Vary exercises for the same muscle across the week (e.g. back squat Monday, hack squat Thursday).
   - Default split for 4 days is upper/lower, Nippard's favourite for size and strength.
   - For a 10-week block, use the shape in `references/programme-patterns.md`: ~5 weeks building, a semi-deload week, then ~5 weeks with rotated exercise variations. Structure sets as early sets (slightly easier) and a last set (to failure on machines, cables and isolation).
   - Use the warm-up table in `references/programme-patterns.md` for the first exercises of each session.
   - Plan a 4–8-week build then a deload week (calculated: −30–50% sets, ~1–3 RPE easier).
   - **Fit the block to the calendar.** Put the deload on a holiday, travel or busy week the pupil mentioned. If the pupil set concrete strength targets, end the block with a test week after the deload.
   - **Fit sessions around other sports and commitments** (from intake): no hard cardio or leg-heavy sport the day before a lower-body session; keep lower days ~72 h apart.
7. **Progression rule** for every exercise: double progression within the rep range (see `progression`).
8. **Present the plan** as one compact table per day (exercise, tier, sets × reps, RPE target, rest, starting weight), with exercise count, set count and expected duration per day. Then a **weekly sets table** with these columns: muscle · points · Shifu target · Nippard range (10–20 for intermediates; hamstrings ~10–15) · **direct sets** · **with indirect (half sets)** · status. Say which counting method each column uses: Nippard counts arm work as direct isolation sets only, while fractional counting (indirect = half) predicted growth best in the research. Never round a gap away. Fill the table from a fresh `sets` run on the final plan, after every revision. Explain the 2–3 most important choices in plain words.
9. **Recount after every revision.** Each time the pupil changes something (an exercise swapped, a set added, a day trimmed), redo the tier column, the per-day counts and duration, and the weekly sets table before presenting again. Don't carry numbers over from the last draft.
10. **Write to Hevy (on confirmation).** Follow `references/hevy.md` ("Writing routines well" and "Account limits"): check `is_pro`, find template IDs with `search_hevy_exercises`, and write one routine per day with rest timers, rep ranges, set types, warm-up sets, starting weights from logs and short this-week notes. On a free account with existing routines, offer to overwrite them (show the mapping, get a yes) rather than creating new ones. Never overwrite without asking.

## Defaults when the user is in a deficit

Offer the lower-volume option (`references/training-science.md`, 100-day experiment): about 1–2 hard sets per exercise, ~6–10 sets per muscle weekly, high effort. Present it as an option with its evidence level.

## Quality checks before presenting

- Every priority muscle hits its weekly set target; nothing exceeds the per-session cap.
- Each day fits the session length at the pupil's real pace, and no day exceeds the exercise cap.
- Every exercise is S/A tier or has a stated reason; the tier column is filled in.
- No avoided exercises; no D/F-tier picks unless the user insists.
- Cues match `references/exercise-tiers.md`.
- The weekly sets table shows direct and indirect counts against both targets, recounted for this version of the plan.
- The deload sits on a holiday or busy week if the pupil named one; sessions don't clash with their other sports.
- Starting weights come from real logs where available; otherwise say "pick a weight you can do for the top of the range with ~2 reps left (RPE 8)".
