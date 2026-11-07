---
name: progression
description: >
  This skill should be used when the user asks "how did my workout go", "should I go up in
  weight", "am I progressing", "I've plateaued", "I'm stuck on X", "do I need a deload",
  "update my weights for next week", or wants a review of recent sessions. It reads Hevy
  history, applies double progression, flags stalls, and proposes next-session targets or
  deloads.
metadata:
  version: "0.1.0"
---

# Progression

Decide the next targets from real data. Never guess logged numbers.

## Steps

1. **Fetch data** (`references/hevy.md`): the last 2–4 sessions of the relevant routine via `get_user_workouts`, and `get_user_exercise_history` for any exercise in question. Fetch the current routine with `get_user_routines`.
   **Evidence window (prevents double changes):** keep a per-exercise change log — current target, date last changed, reason (progression / swap / preference / calibration / deload / user's own change) — wherever the deployment keeps state (a memory file, a notes doc). Judge each exercise only on sessions logged **after** its last change; if there are none, propose nothing for it ("no new data"). A swap or preference change resets the clock and the next session is the new baseline. Before proposing, compare the routine in Hevy with the log: any unexplained difference is the user's own change, dated the routine's `updated_at`; record it, never undo it. After every approved change, update the log. If no log exists yet, create it from the current routines, dated today.
   **Compute it, don't eyeball it:** pass the change log (exercise → changed date, weight, rep range) and the fetched workouts to `scripts/shifu_calc.py evidence`. It counts only sessions after each change, applies the double-progression rules below, and flags stalls. Use its verdicts; override one only with a stated reason (e.g. the user reported pain or poor form).
2. **Apply double progression** per exercise, using the rep range in the routine (default 8–12 if none):
   - All working sets hit the **top** of the range at the planned effort → increase load next session by about 2.5 kg (5 lb) or the next pin; micro-loading is rarely needed.
   - Within the range → keep the load and aim for +1 rep on one or more sets.
   - Below the bottom of the range → keep or reduce load by ~5–10%.
3. **Check effort.** If working sets have a logged `rpe`, use it: top of the range at RPE 7 or below means the load is too light (bigger jump, about two increments); RPE 9.5–10 on `normal` sets of heavy compounds means too close to failure (hold the load, aim for the planned RPE). Without RPE, use set types: If sets marked `normal` repeatedly match the reps of `failure` sets, the early sets are likely at 0–1 RIR (fine for isolation, too hard for compounds). If reps barely drop across sets, effort may be too low.
For numeric strength targets from the pupil card, track estimated 1RMs with `scripts/shifu_calc.py e1rm` (weight, reps, reps left, from the logged RPE where available) rather than guessing.
4. **Detect stalls:** same load and same or fewer reps for **3 consecutive sessions** on an exercise. Then work through, in order:
   1. Technique and effort check (bottom rungs first, `references/principles.md`).
   2. Recovery: sleep, stress, food. Ask if the user is dieting.
   3. Change the rep range (e.g. 6–8 → 10–12) or swap to a similar-tier exercise (`exercise-swaps`).
   4. If several lifts stall at once, or fatigue signs show (weights feel brutally heavy, poor sleep, low motivation, joint aches): deload for a week. Calculated: 30–50% fewer sets (1–2 fewer per exercise), about 1–3 RPE easier; or instinctive: a flexible light week, swapping exercises that felt like a grind. If no deload for ~8 weeks and the user trains hard, suggest one proactively.
5. **Body check (weekly reviews and block reviews):** if weigh-ins or tape measurements are available (from a connected tracker, or ask), compare the weekly average weight and the latest measurements with the previous ones using the table in `references/nutrition.md` ("Reading progress"). Every second week, remind the pupil to measure. Never judge progress on bodyweight alone.
6. **Report** briefly: per exercise, last performance → next target, with one-line reasoning. Lead with wins.
6. **Update Hevy on confirmation.** Change target weights/reps in the routine with `update_hevy_routine`, sending the full routine and changing only those values.

## Example

Hip thrust logged 100 kg × 12, 12, 12, 12 (rep range 8–12): top of range on every set → next session 102.5–105 kg, aim 10+ reps on the first set. If the user picks a specific weight ("make it 105"), use it.

## Rules

- A single bad session is noise; look at trends.
- Counting progress: more reps, more load, or cleaner technique at the same load all count.
- If the user is in a deficit, holding strength is success; don't push load jumps aggressively.
