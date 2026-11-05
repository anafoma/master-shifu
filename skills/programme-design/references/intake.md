---
tags: [intake, profile, questionnaire]
updated: 2026-11-05
---

# The first meeting: pupil questionnaire

Run this the first time Shifu meets a pupil (no saved profile), or when they ask to start over. Keep it warm and quick: four short rounds, multiple choice wherever possible (question cards in the Claude app), and the interactive points widget for round 3. Skip anything already known from the conversation or from Hevy. The pupil can always type freely instead; the exact cards are defined in the intake skill.

## Round 1: who you are

| Question | Format | Used for |
| --- | --- | --- |
| Name (what should I call you?) | Free text | Personal touch |
| Age | Number | Recovery expectations; **if under 18, see safety rules** |
| Height | cm or ft/in | Protein and calorie estimates |
| Bodyweight, and its trend over the last month (stable, rising, falling) | kg or lb + choice | Protein, calories, nutrition phase |
| Sex (optional; "prefer not to say" is fine) | Choice | Only to refine the maintenance-calorie estimate; programming is the same for everyone |

## Round 2: goals

| Question | Format | Used for |
| --- | --- | --- |
| Main goal: muscle size, strength, athletic/explosive, fat loss, or a mix | Choice; if mix, ask for a % split (e.g. 70 size / 20 strength / 10 athletic) | Rep ranges, effort, power work |
| Nutrition phase now: gaining, losing, maintaining, not sure | Choice | Volume tolerance, calories |
| What would make the next 3 months a success? | Free text, one line | Motivation; check expectations are realistic |
| Concrete targets: any numbers to hit (e.g. "squat 80 kg", "hip thrust 120 kg", "train 4× every week") | Free text; prompt for numbers if the answer is vague | Picks the strength lifts, their weekly slot and rep range, the test week, and the realism check against Hevy history |

Concrete numbers shape the programme far more than "build muscle" does: a named lift gets its own heavy slot, a rep range that builds toward the target, and a test at the end of the block. Check each target against the pupil's best logged sets (estimate a 1RM from reps) and say plainly whether it's realistic for the block.

## Round 3: the points game (muscle priorities)

Ask the pupil to share out **20 points** across these muscle groups. More points = more focus. Zero is fine.

Chest · Back (width/lats) · Back (thickness/mid-back) · Shoulders · Arms (biceps + triceps) · Quads · Hamstrings · Glutes · Calves · Abs · Traps/neck

Example: glutes 6, hamstrings 5, shoulders 4, quads 3, back 2, everything else 0.

**Turning points into volume:**

| Points | Role | Weekly hard sets |
| --- | --- | --- |
| 5+ | Top priority (max 3 muscles) | 16–20 (hamstrings capped ~12–15) |
| 3–4 | Priority | 12–16 |
| 1–2 | Grow steadily | 8–12 |
| 0 | Maintain | 4–8 |

If more than 3 muscles get 5+ points, ask which 3 matter most this block; the rest move to "priority". Priority muscles go first in sessions and get trained 2–3×/week.

## Round 4: logistics and history

| Question | Format | Used for |
| --- | --- | --- |
| Training experience: under 6 months, 6–24 months, 2–5 years, 5+ years | Choice | Starting volume, progression model |
| Days per week available | 2–6 | Split |
| Session length | 45 / 60 / 75 / 90 min | Sets per session (with the pupil's real pace, see programme-design) |
| Max exercises per session | 4 / 5 / 6 / 7+ (default 5–6) | Hard cap on exercises per day, separate from the set count |
| Programme length before reassessing | 6 / 8 / 10 / 12 weeks | Block structure |
| Holidays, travel or busy weeks coming up | Choice + dates | Where the deload week goes |
| Other sports, classes or fixed weekly commitments (running, boxing, dance, days that are off-limits) | Choice + text (what, which days) | Schedule, which day each session lands on, cardio placement |
| Where you train (full commercial gym, basic gym, home, mix) | Choice | Starting assumption for equipment; don't ask for a full equipment list |
| Injuries, pain, or exercises you avoid | Free text | Exclusions and swaps (record what to avoid, not diagnoses) |
| Exercises you love or hate | Free text | Adherence |
| Sleep: under 6 h, 6–7 h, 7–8 h, 8+ h | Choice | Recovery expectations |
| Daily activity outside the gym: mostly sitting, some walking, on feet a lot | Choice | Calorie estimate |
| Coaching style: just the plan, short reasons, full explanations | Choice | How much Shifu explains |

**Equipment:** pupils rarely list every machine they have. Don't quiz them. Take the gym type as a starting point, propose specific exercises in the plan, and let the pupil correct anything their gym lacks (programme-design keeps a same-tier fallback ready for each pick).

**Other sports:** place hard cardio and leg-heavy sports away from the day before a lower-body session; light activity (walking, dance classes) can sit on rest days or after upper days. Running is the cardio most likely to interfere with leg training.

## Split by days per week

| Days | Default split |
| --- | --- |
| 2 | Full body ×2 |
| 3 | Full body ×3, or upper/lower/full |
| 4 | Upper/lower ×2 (Nippard's favourite) |
| 5 | Upper/lower + a weak-point/arms day, or push/pull/legs + upper/lower |
| 6 | Push/pull/legs ×2 |

## The pupil card

Finish by showing a compact card and asking the pupil to confirm or correct it:

```
🥋 Pupil: Alex
Body: 170 cm · 65 kg (stable) · experience 2–5 yrs
Goal: size 80 / strength 20 · phase: maintaining
Targets: squat 80 kg · hip thrust 120 kg × 8 · 4 sessions every week
Priorities: glutes 6 · hamstrings 5 · shoulders 4 · quads 3 · back 2
Plan frame: 4 days × 75 min · max 6 exercises · upper/lower · 10-week block · deload over the holidays
Other training: boxing Sun · dance class Mon
Avoid: none · Loves: hip thrusts · Hates: lunges
Sleep 7–8 h · mostly sitting · style: short reasons
Nutrition: tracks in MyFitnessPal · ~2,300 kcal · P 130 g · F 65 g · C 290 g (estimate, check in 2 weeks)
Baseline (5 Nov): waist 69.5 · glutes 99.5 · thigh 56 · upper arm 27 cm · photos taken · re-measure every 2 weeks
```

## Nutrition in onboarding

Nutrition is part of every intake, not an optional extra: training builds muscle only as fast as protein and calories allow. After round 4, ask two things (do you track, and roughly how much protein do you eat), then give the full starting targets (calories, protein, fat, carbs) from the nutrition skill, plus the 2-week tracking homework. Skip this step completely, and give no numbers, if the pupil is under 18 or has mentioned disordered eating, a medical condition, medication or pregnancy (see Rules).

## Rules

- If Hevy is connected, read the last ~10 workouts and the routines first and pre-fill what they show (days per week, session length, loads, favourite exercises). Ask the pupil to confirm instead of asking from scratch.
- Never ask for medical history or diagnoses. Height, weight and age are used only for training and nutrition numbers.
- **Under 18:** keep the questionnaire, but no calorie deficits or bulking targets; focus on technique, moderate effort and enough food and sleep; suggest involving a parent, coach or doctor for nutrition.
- If the pupil mentions disordered eating, don't ask for weight or give calorie numbers; follow the nutrition skill's safety rules.
- If the pupil says "you decide" for any question, choose a sensible default and mark it with "(Shifu's pick)" on the card.
- The profile belongs to the person in the conversation. Never mix two pupils' data.
