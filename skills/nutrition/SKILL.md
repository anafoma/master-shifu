---
name: nutrition
description: >
  This skill should be used when the user asks about protein, calories, macros, bulking,
  cutting, recomposition, "how much should I eat", "how fast should I lose weight", "should
  I bulk", supplements such as creatine, or how diet should change their training. It gives
  evidence-based targets and adjusts training for the nutrition phase.
metadata:
  version: "0.1.0"
---

# Nutrition

Give practical targets from `references/nutrition.md`. Keep it simple: protein and energy balance first, everything else second.

## Steps

1. **Establish the phase:** bulking, cutting, maintaining or recomposition, plus bodyweight and its recent trend (ask if unknown). Training age matters for bulking rates.
2. **Protein:** 1.6–2.2 g/kg/day; top of the range in a deficit. Show the number in grams for their bodyweight, and a simple split (e.g. 4 meals × ~0.4 g/kg).
3. **Energy:**
   - Bulk: aim for a weight gain rate of 1–2%/month (beginners) or 0.5–1%/month (intermediate+), roughly a 5–10% surplus for a lean bulk.
   - Cut: about 0.5–0.7% of bodyweight per week, roughly a 500 kcal/day deficit.
   - Maintenance/recomp: hold weight within ~1%; prioritise protein and training.
   - Prefer adjusting by trend: check the 2-week average weight change and move intake by ~100–200 kcal/day if off-target.
4. **Adjust training to the phase:** in a cut, keep effort high and offer lower volume (see `references/training-science.md`); expect strength to hold rather than climb.
5. **Supplements:** creatine monohydrate (strongest evidence), caffeine for performance; protein powder is just convenient food.

## Hard limits

- No targets below safe levels and no crash diets. Never go below the cut rate above.
- If the user mentions a medical condition, medication, pregnancy, or disordered eating, don't give numeric targets; recommend a doctor or registered dietitian, kindly and briefly.
- Not medical advice: say so once if the user asks for anything clinical.
