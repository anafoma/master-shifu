---
name: nutrition
description: >
  This skill should be used when the user asks about protein, calories, macros, bulking,
  cutting, recomposition, "how much should I eat", "how fast should I lose weight", "should
  I bulk", supplements such as creatine, or how diet should change their training. It gives
  evidence-based targets and adjusts training for the nutrition phase.
metadata:
  version: "0.10.0"
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
   - Estimate maintenance first: Mifflin-St Jeor × activity factor when height, age and sex are known, cross-checked with kg × 31–40 (`references/nutrition.md`). Say it's an estimate (±200 kcal) that 2 weeks of tracking will correct.
   - Prefer adjusting by trend: check the 2-week average weight change and move intake by ~100–200 kcal/day if off-target.
   - **Always finish with the full set:** calories, protein, fat and carbs in grams per day, built protein → fat → carbs as in "From calories to macros", with the arithmetic checked by `scripts/shifu_calc.py macros` (sex, age, weight, height, activity factor, then either a calorie target or `adjust_pct`, plus protein and fat choices). Quote its BMR, maintenance and grams; it enforces the fat floor and the calorie check. Show the numbers for the current phase and, if a phase change is on the table, for the alternative too.
4. **Adjust training to the phase:** in a cut, keep effort high and offer lower volume (see `references/training-science.md`); expect strength to hold rather than climb.
5. **Make it stick:** offer 1–2 habit tools that fit the user (non-tracking tools, meal structure, evening plan) from `references/nutrition.md`, and after a cut, plan the move back to maintenance.
6. **Supplements:** creatine monohydrate (strongest evidence), caffeine for performance; protein powder is just convenient food.

## Logging food day to day

If a nutrition tracker is connected (`references/connections.md`), use it as much as possible: log every meal the pupil describes, photographs or shows a label for; read labels exactly and scale to the amount eaten; confirm portions and hidden extras (oil, sauces, drinks) before logging unless the pupil says "just log it"; log water too. Correct entries when the pupil corrects you (e.g. leftovers, a different cut of meat). Plan social days by getting most of the protein in early and leaving calories for the evening; calories are judged on the weekly average. If no tracker is connected, give the numbers in chat and offer the setup.

## Hard limits

- No targets below safe levels and no crash diets. Never go below the cut rate above.
- If the user mentions a medical condition, medication, pregnancy, or disordered eating, don't give numeric targets; recommend a doctor or registered dietitian, kindly and briefly.
- Not medical advice: say so once if the user asks for anything clinical.
