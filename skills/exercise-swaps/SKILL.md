---
name: exercise-swaps
description: >
  This skill should be used when the user asks "what can I do instead of X", "X hurts my
  knee/shoulder/back", "the machine is taken", "I don't have a cable", "I'm bored of X",
  "is X a good exercise", or asks for a tier or ranking of an exercise. It finds a
  replacement of similar tier, muscle target and stretch profile, or rates an exercise
  using Nippard's three criteria.
metadata:
  version: "0.1.0"
---

# Exercise swaps

## Swapping an exercise

1. **Identify why:** pain, equipment, crowding, boredom, or plateau. Pain changes the rules (below).
2. **Find candidates** in `references/exercise-tiers.md` for the same target muscle and a similar role (compound vs isolation, stretch-focused vs shortened).
3. **Rank candidates:** same or higher tier → similar stretch under tension → fits the user's equipment → easy to progress → least overlap with joints that hurt.
4. **Offer 1 main pick and 1–2 alternatives**, one line each with the reason. Example: "Seated leg curl → if the machine is taken, lying leg curl (A, slightly less growth per research) or RDL (more fatigue, also hits glutes)."
5. **Update Hevy on confirmation:** find the new template with `search_hevy_exercises`, then replace the exercise in the routine via `update_hevy_routine`, sending the full routine. Set a conservative starting weight (or none) and the same rep range.

## When it hurts

- Swap to a variation that loads the muscle with less stress on the painful joint (e.g. knee pain on squats → leg press with limited depth, or leg extension; shoulder pain on pressing → machine press with neutral grip, reduced range).
- If pain is sharp, persists after the swap, or affects daily life, recommend a physio or doctor. Never diagnose.

## Rating an exercise Nippard never ranked

Score it on the three criteria in `references/principles.md` (stretch under tension, feels good, simple progression), give a tier with one sentence of reasoning, and say it's Shifu's estimate, not Nippard's ranking.
