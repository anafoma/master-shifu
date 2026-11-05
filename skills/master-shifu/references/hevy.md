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
6. **Set types:** treat `failure` sets as 0 RIR; `warmup` sets don't count toward volume.
7. **Session time:** end_time − start_time gives real session length; use it to check the plan fits.
