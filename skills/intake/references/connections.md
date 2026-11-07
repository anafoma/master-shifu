---
tags: [setup, connectors, nutrition, wearables]
updated: 2026-11-07
---

# Connections: what Shifu can plug into

Shifu works best with three connections. Only Hevy is required; the other two make coaching sharper. Check what's connected at the start of every intake, before asking questions, and help the pupil set up what's missing in a few plain steps. Never block the intake on a connection: if the pupil wants to skip, carry on and offer again later.

Tool names carry a prefix that varies by setup (e.g. `mcp__Hevy__get_user_workouts`, `mcp__Nutrition__log_meal`); match on the part after the last `__`.

## How to tell what's connected

| Connection | Present if you can see tools like | Without it |
| --- | --- | --- |
| Workout log (Hevy) | `get_user_workouts`, `get_user_routines` | Shifu can design a plan but can't read history or write routines |
| Nutrition tracker | `log_meal`, `get_goal_progress`, `set_nutrition_goals` | Targets still given; logging and daily progress are by hand |
| Wearable (watch/ring) | sleep, HRV, heart-rate or steps tools (e.g. `get_sleep`, `get_hrv`) | No sleep/recovery data; ask how the pupil slept instead |

If a connection is missing, say so in one line and offer the setup steps below. If the session has a connector-search tool (e.g. `SearchMcpRegistry` / `SuggestConnectors`), use it to offer a one-click connect before giving manual steps.

## 1. Hevy (required)

- In Claude: Settings → Connectors → find **Hevy** in the connector directory and connect (if it isn't listed, ask the person who shared the plugin how they added it), then sign in with the pupil's own Hevy account.
- Free Hevy accounts work (limits on routines and custom exercises; see [[hevy]], "Account limits").
- After connecting, the pupil should start a new chat (new tools load at the start of a chat).

## 2. Nutrition tracker (strongly recommended)

Shifu's default is **Nutrition MCP**, a free remote connector that logs meals (from photos, labels or text), water, weight and body measurements, and tracks progress against goals.

- In Claude: Settings → Connectors → **Add custom connector**, URL `https://nutrition-mcp.com/mcp`, then sign in when asked.
- Start a new chat after connecting.

**First use (once, after the intake gives targets):**
1. Set the pupil's timezone and units (kg/lb, cm/in).
2. Save the targets from the nutrition skill with `set_nutrition_goals` (calories, protein, fat, carbs, water).
3. Log the baseline weight and tape measurements (`log_weight`, `log_body_measurement`).

If the pupil already uses another tracker (MyFitnessPal, Cronometer…), check for a connector for it first; if there's none, offer Nutrition MCP or carry on with targets only.

## 3. Wearable (optional)

Ask: **"Do you wear a watch or ring that tracks sleep and heart rate? Which one?"** Then:

- **Search for a connector** for that brand first (connector-search tool if present). Use an official or well-maintained connector when one exists.
- **Garmin:** there's no official Claude connector at the time of writing. A community project, `garmin-personal-mcp`, runs on the pupil's own computer: it needs the Claude desktop app open on that computer, Python's `uv` installed, and a Garmin Connect login. It's a small project, so say so and let the pupil decide. Data only flows while that computer is on with the Claude desktop app running.
- **Any other brand with no connector:** skip it. Shifu works fine without a wearable; ask "how did you sleep?" in reviews instead.

Whatever the watch, remind the pupil to **wear it at night** (sleep and HRV) and, if they like, in the gym. Training load still comes from the workout log, not the watch.

## Order in the intake

1. Check connections silently (tools present?).
2. In the greeting, say what's connected and what's missing in one or two lines.
3. Offer setup for Hevy first if missing (needed for the plan), then nutrition, then the wearable. Ask about the wearable only once.
4. Continue the intake either way; set up the nutrition tracker's goals at step 7, once targets exist.
