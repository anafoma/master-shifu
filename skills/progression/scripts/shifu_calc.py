#!/usr/bin/env python3
"""Master Shifu calculator: deterministic maths for the coaching skills.

The skills must call this instead of doing arithmetic in their heads.
Standard library only. JSON in (file path or "-" for stdin), JSON out.

    python3 shifu_calc.py <command> <input.json | ->

Commands:
    sets      weekly sets per muscle (direct and fractional) against targets
    budget    real pace (min/set) from logged workouts and expected session length
    macros    Mifflin-St Jeor maintenance and calories -> protein, fat, carbs
    e1rm      estimated one-rep max from a weight x reps set
    evidence  per-exercise evidence window + double-progression suggestion

Every command validates its input and exits 2 with {"error": ...} on bad data.
"""
from __future__ import annotations

import json
import statistics
import sys
from datetime import datetime, timezone

VERSION = "1.0.0"


class InputError(ValueError):
    pass


def _need(d: dict, key: str, kind=None):
    if key not in d:
        raise InputError(f"missing field: {key}")
    v = d[key]
    if kind is not None and not isinstance(v, kind):
        raise InputError(f"field {key} must be {kind}")
    return v


def _num(d: dict, key: str, default=None, lo=None, hi=None) -> float:
    if key not in d:
        if default is None:
            raise InputError(f"missing field: {key}")
        return default
    v = d[key]
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        raise InputError(f"field {key} must be a number")
    if lo is not None and v < lo:
        raise InputError(f"field {key} must be >= {lo}")
    if hi is not None and v > hi:
        raise InputError(f"field {key} must be <= {hi}")
    return float(v)


def _r(x: float, nd: int = 1) -> float:
    return round(x + 0.0, nd)


def _round_to(x: float, step: float) -> float:
    return round(x / step) * step


# --------------------------------------------------------------------- sets
def cmd_sets(data: dict) -> dict:
    """Input:
    {"days": [{"name": "Lower A", "exercises": [
        {"name": "Hip Thrust", "sets": 4, "primary": ["glutes"], "secondary": ["hamstrings"]}]}],
     "targets": {"glutes": [16, 20]},             # Shifu target per muscle (optional)
     "isolation_only": ["biceps", "triceps"],      # Nippard: arms count direct isolation only
     "indirect_weight": 0.5}
    An exercise counts fully for each `primary` muscle and `indirect_weight` for each `secondary`.
    """
    days = _need(data, "days", list)
    targets = data.get("targets", {}) or {}
    iso_only = set(data.get("isolation_only", ["biceps", "triceps"]))
    w = _num(data, "indirect_weight", 0.5, 0, 1)
    direct: dict[str, float] = {}
    fractional: dict[str, float] = {}
    nippard: dict[str, float] = {}
    per_day = []
    for day in days:
        exs = _need(day, "exercises", list)
        day_sets = 0.0
        per_muscle_day: dict[str, float] = {}
        for ex in exs:
            n = _num(ex, "sets", lo=0)
            prim = ex.get("primary", [])
            sec = ex.get("secondary", [])
            if not prim:
                raise InputError(f"exercise {ex.get('name', '?')} has no primary muscle")
            day_sets += n
            for m in prim:
                direct[m] = direct.get(m, 0) + n
                fractional[m] = fractional.get(m, 0) + n
                per_muscle_day[m] = per_muscle_day.get(m, 0) + n
                # Nippard method: compounds don't count for arms; isolation does.
                if m not in iso_only or len(prim) == 1:
                    nippard[m] = nippard.get(m, 0) + n
            for m in sec:
                fractional[m] = fractional.get(m, 0) + n * w
                direct.setdefault(m, 0)
                nippard.setdefault(m, 0)
        over = {m: s for m, s in per_muscle_day.items() if s > 8}
        per_day.append({
            "name": day.get("name", "?"),
            "exercises": len(exs),
            "sets": _r(day_sets),
            "muscles_over_8_direct_sets": over,
        })
    muscles = sorted(set(direct) | set(fractional) | set(targets))
    rows = []
    for m in muscles:
        row = {
            "muscle": m,
            "direct": _r(direct.get(m, 0)),
            "nippard_count": _r(nippard.get(m, 0)),
            "fractional": _r(fractional.get(m, 0)),
        }
        if m in targets:
            lo, hi = targets[m]
            f = fractional.get(m, 0)
            row["target"] = [lo, hi]
            row["status"] = "below" if f < lo else ("above" if f > hi else "in range")
            row["gap"] = _r(lo - f) if f < lo else 0
        rows.append(row)
    total = sum(d["sets"] for d in per_day)
    return {"muscles": rows, "days": per_day, "weekly_sets": _r(total),
            "target_sum_low": sum(t[0] for t in targets.values()) if targets else None}


# ------------------------------------------------------------------- budget
def _parse_ts(s: str) -> datetime:
    s = s.replace("Z", "+00:00")
    dt = datetime.fromisoformat(s)
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def cmd_budget(data: dict) -> dict:
    """Input:
    {"workouts": [{"start_time": iso, "end_time": iso, "sets": 18, "title": "..."}],
     "default_pace": 4.0,
     "session_minutes": 75,
     "plan": [{"name": "Upper A", "exercises": 6, "sets": 17}],
     "exercise_cap": 6}
    Hevy workouts can be passed raw: if "sets" is absent, sets are counted from
    exercises[].sets excluding warm-ups. Sessions longer than 3 h, shorter than
    10 min, or with a pace outside 1.5-9 min/set are skipped as "forgot to stop".
    """
    workouts = data.get("workouts", []) or []
    default_pace = _num(data, "default_pace", 4.0, 1, 10)
    paces, skipped = [], []
    for wk in workouts:
        try:
            mins = (_parse_ts(wk["end_time"]) - _parse_ts(wk["start_time"])).total_seconds() / 60
        except (KeyError, ValueError) as e:
            raise InputError(f"workout needs start_time and end_time: {e}")
        if "sets" in wk:
            n = wk["sets"]
        else:
            n = sum(1 for ex in wk.get("exercises", []) for s in ex.get("sets", [])
                    if s.get("type", "normal") != "warmup")
        title = wk.get("title", wk.get("start_time"))
        if n <= 0 or mins < 10 or mins > 180:
            skipped.append({"workout": title, "reason": "duration or set count implausible"})
            continue
        p = mins / n
        if not 1.5 <= p <= 9:
            skipped.append({"workout": title, "reason": f"pace {p:.1f} min/set implausible"})
            continue
        paces.append(p)
    if paces:
        pace = statistics.median(paces)
        source = f"median of {len(paces)} logged sessions"
    else:
        pace = default_pace
        source = "default (no usable history)"
    out = {"pace_min_per_set": _r(pace, 2), "pace_source": source, "skipped": skipped}
    if "session_minutes" in data:
        sm = _num(data, "session_minutes", lo=10)
        out["sets_that_fit"] = int(sm // pace)
    cap = data.get("exercise_cap")
    plan_out = []
    for day in data.get("plan", []) or []:
        sets = _num(day, "sets", lo=0)
        row = {"name": day.get("name", "?"), "sets": sets,
               "expected_minutes": round(sets * pace)}
        if "session_minutes" in data:
            row["fits_time"] = row["expected_minutes"] <= data["session_minutes"]
        if cap is not None and "exercises" in day:
            row["exercises"] = day["exercises"]
            row["within_exercise_cap"] = day["exercises"] <= cap
        plan_out.append(row)
    if plan_out:
        out["plan"] = plan_out
    return out


# ------------------------------------------------------------------- macros
ACTIVITY = {"sedentary": 1.2, "light": 1.375, "moderate": 1.55, "active": 1.725, "very_active": 1.9}


def cmd_macros(data: dict) -> dict:
    """Input:
    {"sex": "female" | "male" | "unspecified", "age": 30, "weight_kg": 62, "height_cm": 168,
     "activity_factor": 1.5 | "moderate",
     "calories": 2000,                 # optional override of the target
     "adjust_pct": -10,                # optional: % from maintenance (cut <0, bulk >0)
     "protein_g_per_kg": 2.0 | "protein_g": 120,
     "fat_g_per_kg": 0.9 | "fat_pct": 25,
     "fat_floor_g_per_kg": 0.6}
    Order: protein -> fat -> carbs from the remainder. Rounded to 5 g / 10 kcal.
    """
    sex = str(data.get("sex", "unspecified")).lower()
    if sex not in ("female", "male", "unspecified"):
        raise InputError("sex must be female, male or unspecified")
    age = _num(data, "age", lo=14, hi=100)
    kg = _num(data, "weight_kg", lo=30, hi=300)
    cm = _num(data, "height_cm", lo=120, hi=230)
    af = data.get("activity_factor", 1.5)
    if isinstance(af, str):
        if af not in ACTIVITY:
            raise InputError(f"activity_factor must be a number or one of {sorted(ACTIVITY)}")
        af = ACTIVITY[af]
    af = _num({"a": af}, "a", lo=1.1, hi=2.4)
    bmr = 10 * kg + 6.25 * cm - 5 * age + {"male": 5, "female": -161, "unspecified": -78}[sex]
    maintenance = bmr * af
    if "calories" in data:
        kcal = _num(data, "calories", lo=1000, hi=6000)
        basis = "given"
    else:
        adj = _num(data, "adjust_pct", 0, -30, 30)
        kcal = maintenance * (1 + adj / 100)
        basis = f"maintenance {adj:+g}%"
    kcal = _round_to(kcal, 10)

    if "protein_g" in data:
        p = _num(data, "protein_g", lo=20, hi=400)
    else:
        p = kg * _num(data, "protein_g_per_kg", 1.8, 1.0, 3.0)
    p = _round_to(p, 5)

    floor = _round_to(kg * _num(data, "fat_floor_g_per_kg", 0.6, 0.3, 1.5), 5)
    if "fat_pct" in data:
        f = kcal * _num(data, "fat_pct", lo=15, hi=45) / 100 / 9
    else:
        f = kg * _num(data, "fat_g_per_kg", 0.9, 0.4, 2.0)
    f = max(_round_to(f, 5), floor)

    c = _round_to((kcal - p * 4 - f * 9) / 4, 5)
    warnings = []
    if c < 0:
        raise InputError("protein and fat exceed the calorie target; lower one of them")
    if c / kg < 3:
        warnings.append(f"carbs {c / kg:.1f} g/kg is below the ~3 g/kg typical for lifters")
    check = p * 4 + f * 9 + c * 4
    return {
        "bmr": round(bmr), "activity_factor": af, "maintenance_kcal": _round_to(maintenance, 10),
        "target_kcal": kcal, "target_basis": basis,
        "protein_g": p, "fat_g": f, "carbs_g": c,
        "per_kg": {"protein": _r(p / kg, 2), "fat": _r(f / kg, 2), "carbs": _r(c / kg, 2)},
        "fat_pct_of_kcal": _r(f * 9 / kcal * 100),
        "arithmetic_check_kcal": check, "check_diff_kcal": check - kcal,
        "fat_floor_g": floor, "warnings": warnings,
    }


# --------------------------------------------------------------------- e1rm
def cmd_e1rm(data: dict) -> dict:
    """Input: {"weight_kg": 60, "reps": 5, "rir": 0}. Reps-in-reserve are added to reps."""
    w = _num(data, "weight_kg", lo=0.5)
    reps = _num(data, "reps", lo=1, hi=30)
    rir = _num(data, "rir", 0, 0, 6)
    r = reps + rir
    epley = w * (1 + r / 30) if r > 1 else w
    brzycki = w * 36 / (37 - r) if r > 1 else w
    out = {"epley": _r(epley), "brzycki": _r(brzycki), "estimate": _r((epley + brzycki) / 2),
           "effective_reps": r}
    if r > 12:
        out["warning"] = "estimates above ~12 reps are unreliable"
    return out


# ----------------------------------------------------------------- evidence
def cmd_evidence(data: dict) -> dict:
    """Input:
    {"log": {"Hip Thrust (Barbell)": {"changed": "2026-11-05", "weight_kg": 105,
                                       "rep_range": [6, 10], "sets": 4, "reason": "calibration"}},
     "workouts": [Hevy workouts with start_time and exercises[].title / sets[]],
     "increment_kg": 2.5}
    For each logged exercise: only sessions strictly after `changed` count. With none,
    the verdict is "no new data". Otherwise double progression is applied to the most
    recent session's working sets at (or above) the target weight.
    """
    log = _need(data, "log", dict)
    workouts = data.get("workouts", []) or []
    inc = _num(data, "increment_kg", 2.5, 0.5, 20)
    results = []
    for name, entry in log.items():
        changed = _need(entry, "changed", str)
        try:
            cdate = datetime.fromisoformat(changed).date()
        except ValueError:
            raise InputError(f"{name}: changed must be YYYY-MM-DD")
        lo, hi = entry.get("rep_range", [8, 12])
        target = entry.get("weight_kg")
        sessions = []
        for wk in workouts:
            day = _parse_ts(wk["start_time"]).date()
            if day <= cdate:
                continue
            for ex in wk.get("exercises", []):
                if ex.get("title") != name:
                    continue
                work = [s for s in ex.get("sets", []) if s.get("type", "normal") != "warmup"
                        and s.get("reps") is not None]
                if work:
                    sessions.append({"date": day.isoformat(), "sets": [
                        {"weight_kg": s.get("weight_kg"), "reps": s["reps"],
                         "type": s.get("type", "normal")} for s in work]})
        sessions.sort(key=lambda s: s["date"])
        row = {"exercise": name, "changed": changed, "sessions_in_window": len(sessions)}
        if not sessions:
            row.update(verdict="no new data", action="hold", next_weight_kg=target)
            results.append(row)
            continue
        last = sessions[-1]
        sets = last["sets"]
        weights = [s["weight_kg"] for s in sets if s["weight_kg"] is not None]
        used = max(weights) if weights else None
        reps = [s["reps"] for s in sets]
        row["last_session"] = last
        if target is not None and used is not None and used < target:
            row.update(verdict="below planned weight", action="hold",
                       next_weight_kg=target, note=f"used {used} kg vs planned {target} kg")
        elif all(r >= hi for r in reps):
            base = used if used is not None else target
            row.update(verdict="top of range on every set", action="increase",
                       next_weight_kg=None if base is None else base + inc)
        elif min(reps) < lo:
            base = used if used is not None else target
            row.update(verdict="below bottom of range", action="hold or reduce 5-10%",
                       next_weight_kg=base,
                       reduced_weight_kg=None if base is None else _round_to(base * 0.925, inc))
        else:
            row.update(verdict="within range", action="add reps",
                       next_weight_kg=used if used is not None else target)
        # stall: same load, same or fewer total reps, 3 consecutive sessions
        if len(sessions) >= 3:
            last3 = sessions[-3:]
            loads = {max((s["weight_kg"] or 0) for s in x["sets"]) for x in last3}
            totals = [sum(s["reps"] for s in x["sets"]) for x in last3]
            if len(loads) == 1 and totals[2] <= totals[1] <= totals[0]:
                row["stall"] = True
        results.append(row)
    return {"exercises": results}


COMMANDS = {"sets": cmd_sets, "budget": cmd_budget, "macros": cmd_macros,
            "e1rm": cmd_e1rm, "evidence": cmd_evidence}


def run(command: str, data: dict) -> dict:
    if command not in COMMANDS:
        raise InputError(f"unknown command {command}; use one of {sorted(COMMANDS)}")
    if not isinstance(data, dict):
        raise InputError("input must be a JSON object")
    out = COMMANDS[command](data)
    out["_tool"] = {"name": "shifu_calc", "version": VERSION, "command": command}
    return out


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(__doc__)
        return 0 if len(argv) >= 2 else 2
    command = argv[1]
    src = argv[2] if len(argv) > 2 else "-"
    try:
        raw = sys.stdin.read() if src == "-" else open(src, encoding="utf-8").read()
        data = json.loads(raw)
        print(json.dumps(run(command, data), indent=2))
        return 0
    except (InputError, json.JSONDecodeError, OSError) as e:
        print(json.dumps({"error": str(e)}))
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
