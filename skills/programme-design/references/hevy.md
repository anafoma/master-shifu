---
tags: [hevy, tools]
updated: 2026-11-05
---

# Working with Hevy

Hevy is the user's workout log, connected as an MCP connector. Tool names may carry a prefix (e.g. `mcp__Hevy__get_user_workouts`); match on the suffix. If no Hevy tools are present, ask the user to connect Hevy in Claude's connector settings and carry on with what they tell you.

## Read tools

| Tool | Use it for |
| --- | --- |
| `get_user_workouts` (page, pageSize ≤ 10) | Recent sessions, newest first: sets, reps, weight, set type (warmup/normal/failure/dropset), start/end time |
| `get_user_routines` | The user's saved routines (their current programme) with target sets/reps/weights |
| `get_user_exercise_history` | One exercise's history over time; best for progression and stall checks |
| `search_hevy_exercises` | Find `exercise_template_id`s by name before creating or editing routines |
| `get_hevy_routine_folders` | Folder structure, e.g. one folder per programme block |
| `get_user_preferences` | Units (kg/lb) and other settings |

## Write tools

| Tool | Use it for |
| --- | --- |
| `update_hevy_routine` | Change an existing routine (e.g. new target weight) |
| `create_hevy_routine` / `create_hevy_routine_folder` | Build a new programme |
| `create_custom_exercise` | Only when no template exists |
| `create_hevy_plan` / `render_hevy_plan` | Multi-routine plans, where available |

## Display tools

`render_hevy_workouts` and `render_hevy_routine` show cards in the chat. After rendering, don't repeat the card's contents; add one or two sentences of coaching.

## Rules

1. **Read before writing.** Fetch the routine fresh just before updating. Someone (the user or another session) may have changed it.
2. **`update_hevy_routine` replaces the whole routine.** Send every exercise and set, changing only what was agreed. Dropping an exercise by accident deletes it from the user's plan.
3. **Confirm writes.** Before creating or changing routines, state the change in one line and get a yes, unless the user's message already asked for exactly that change.
4. **Report surprises.** If the routine differs from the last logged workout (e.g. an exercise swapped since), mention it.
5. **Units:** Hevy stores `weight_kg`. Convert if the user's preference is lb.
6. **Set types and effort:** treat `failure` sets as RPE 10 (0 RIR); `warmup` sets don't count toward volume. If logged sets carry an `rpe` value, use it as the effort measure (RPE = 10 − reps left); otherwise fall back to set types.
7. **Session time:** end_time − start_time gives real session length; use it to check the plan fits. Divide by the sets logged to get the pupil's real pace per set (see programme-design). Ignore sessions with notes like "forgot to stop the workout".

## Writing routines well

Every routine Shifu writes should be usable mid-workout without opening the chat:

- **Rest timer on every exercise** (`rest_seconds`), by type: heavy compounds (squat, hip thrust, deadlift variants) 180–210 s; other compounds and presses 120–150 s; isolation 75–90 s; abs and calves 60–75 s. Hevy starts it automatically when a set is ticked.
- **Rep ranges, not single numbers:** use `rep_range: {start, end}` on working sets (e.g. 8–10), leave `reps` empty.
- **Set types:** `warmup` for ramp-up sets, `normal` for working sets, `failure` only on the sets meant to go to failure (usually the last set of machine, cable and isolation work). Never mark heavy free-weight compounds as failure.
- **Warm-up sets** before the first heavy lift of the session (and the first press on upper days), using the warm-up table in programme-patterns (e.g. ~50% × 8, ~75% × 5).
- **Starting weights:** from the pupil's logs where the exercise (or a close variant) exists. For a new exercise, leave `weight_kg` empty and tell the pupil the rule: "pick a weight you can do for the top of the range with ~2 reps left".
- **Notes: short and about this week only.** One line per exercise, max ~15 words: effort target plus one cue, e.g. "RPE 8–9 · 1 s squeeze at the top" or "Last set RPE 10 · sit tall". No future weeks, block timelines or progression rules in notes; they make the routine busy and go stale. Routine note: one line ("Week 3 · build"). Weights and rep ranges go in the sets, not the notes.
- **Effort targets go in the note, as RPE.** Routines have no target-effort field, but logged sets do have an RPE field. Write the target as RPE (RPE = 10 − reps left: 1–2 left = RPE 8–9, failure = RPE 10) so it matches what the pupil logs, and ask them to log RPE on working sets (not warm-ups); it may need turning on in Hevy's settings. Reviews can then tell fatigue from under-effort.
- **Exercise names:** search the library first with several phrasings (`search_hevy_exercises` accepts a list). Some popular exercises are missing or named differently (e.g. the Bayesian curl is not in the library; "Behind the Back Curl (Cable)" is the closest). Ask before creating a custom exercise.

## Account limits

Check `get_user_preferences` → `is_pro` before building.

- **Free accounts have a routine cap.** If the pupil is on a free account and already has routines, don't stack new ones on top. Offer to **overwrite** existing routines instead: show the mapping ("Quads & Calves → Lower A, Upper → Upper A…"), explain that the old routine contents are replaced but logged workout history is kept, and get an explicit yes.
- **No delete tool.** Routines can't be deleted through the connector; the pupil deletes them in the app. Overwriting avoids the need.
- **Custom exercises: free accounts are limited to 7.** Use library templates whenever one fits; create a custom exercise only when the pupil asks for something the library lacks, and tell them it was added.
- **Folders** are optional; don't create one if the pupil only needs a few routines.
- A new or custom exercise starts with no history; old logs stay under the old exercise name. Mention this when swapping.
- **Routines have no per-exercise "last changed" date** (only the routine's `updated_at`), so Hevy alone can't tell which exercise changed or why. Keep a change log outside Hevy (see the progression skill's evidence-window rule) and add a one-line "Last review: <date>" to the routine note when a review changes it.
