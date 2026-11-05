# Master Shifu

An evidence-based gym coach plugin for Claude, inspired by Jeff Nippard's science-based approach to hypertrophy and strength. Master Shifu runs intake, designs programmes, reads your Hevy logs to plan progression, swaps exercises, and covers nutrition basics.

> Master Shifu is an independent personal project. It is not affiliated with or endorsed by Jeff Nippard.

## What's inside

| Part | Purpose |
| --- | --- |
| `skills/master-shifu` | Coach persona, core principles, routing to the other skills |
| `skills/intake` | Nine-question intake → confirmed training profile |
| `skills/programme-design` | Split, weekly sets per muscle, exercise picks, Hevy routines |
| `skills/specialisation` | Prioritise lagging muscles for a block |
| `skills/progression` | Double progression, stall detection, deloads from Hevy history |
| `skills/exercise-swaps` | Like-for-like replacements; rate any exercise |
| `skills/nutrition` | Protein, bulking and cutting rates, supplements |
| `agents/master-shifu.md` | Multi-step coaching agent (Claude Code) |
| `knowledge/programme-patterns.md` | High-level methods from Nippard's paid programmes (no workouts reproduced) |
| `knowledge/` | Single source of truth for the knowledge base (open as an Obsidian vault) |
| `evals/scenarios.json` | Test prompts with expected behaviour |

## Requirements

- **Hevy connector** in your Claude account. Each person connects their own Hevy. Free accounts work, with limits on routines and custom exercises (see `knowledge/hevy.md`, "Account limits").
- Later: a health-data connector (sleep, HRV, resting heart rate) for readiness-based adjustments.

## Editing the knowledge

1. Open `knowledge/` in Obsidian and edit.
2. Run `./scripts/sync-knowledge.sh` to copy the files into each skill's `references/`.
3. Rerun the evals, bump the version in `.claude-plugin/plugin.json`, then rebuild and reinstall.

Keep knowledge files paraphrased with links. Don't paste transcripts or book text.

## Build and install

```bash
./scripts/sync-knowledge.sh
./scripts/build.sh          # writes dist/master-shifu.plugin
```

Upload `dist/master-shifu.plugin` in Claude's plugin settings. In Claude Code, add this repo as a plugin marketplace or install the plugin from it.

## Running evals

Open a fresh chat with the plugin installed, paste each scenario's `prompt`, and check every line in `expect`. Note failures, fix the skill or knowledge file, and rerun.
