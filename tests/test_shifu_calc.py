"""Unit tests for tools/shifu_calc.py. Run: python3 -m unittest discover -s tests"""
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import shifu_calc as sc  # noqa: E402


def wk(start, end, exercises=None, sets=None, title="W"):
    d = {"title": title, "start_time": start, "end_time": end}
    if exercises is not None:
        d["exercises"] = exercises
    if sets is not None:
        d["sets"] = sets
    return d


class TestMacros(unittest.TestCase):
    def test_female_given_calories(self):
        out = sc.run("macros", {"sex": "female", "age": 30, "weight_kg": 62, "height_cm": 168,
                                "activity_factor": 1.5, "calories": 2000, "protein_g": 120,
                                "fat_g_per_kg": 0.9})
        self.assertEqual(out["bmr"], 1359)  # 620 + 1050 - 150 - 161
        self.assertEqual(out["maintenance_kcal"], 2040)
        self.assertEqual((out["protein_g"], out["fat_g"], out["carbs_g"]), (120, 55, 255))
        self.assertLessEqual(abs(out["check_diff_kcal"]), 20)

    def test_unspecified_sex_uses_midpoint(self):
        out = sc.run("macros", {"age": 30, "weight_kg": 62, "height_cm": 168})
        self.assertEqual(out["bmr"], 1442)  # midpoint constant -78

    def test_male_formula_and_cut(self):
        out = sc.run("macros", {"sex": "male", "age": 30, "weight_kg": 80, "height_cm": 180,
                                "activity_factor": "moderate", "adjust_pct": -20})
        self.assertEqual(out["bmr"], 1780)  # 800 + 1125 - 150 + 5
        self.assertEqual(out["target_kcal"], 2210)  # 1780*1.55*0.8 = 2207.2
        self.assertLessEqual(abs(out["check_diff_kcal"]), 20)

    def test_fat_floor_enforced(self):
        out = sc.run("macros", {"sex": "female", "age": 27, "weight_kg": 60, "height_cm": 165,
                                "calories": 1800, "fat_pct": 15, "fat_floor_g_per_kg": 0.8})
        self.assertEqual(out["fat_g"], 50)  # 15% would be 30 g; floor is 48 -> 50

    def test_impossible_split_rejected(self):
        with self.assertRaises(sc.InputError):
            sc.run("macros", {"sex": "female", "age": 27, "weight_kg": 60, "height_cm": 165,
                              "calories": 1000, "protein_g": 200, "fat_g_per_kg": 1.5})

    def test_bad_sex(self):
        with self.assertRaises(sc.InputError):
            sc.run("macros", {"sex": "x", "age": 27, "weight_kg": 60, "height_cm": 165})


class TestSets(unittest.TestCase):
    PLAN = {
        "days": [
            {"name": "Lower B", "exercises": [
                {"name": "Hip Thrust", "sets": 4, "primary": ["glutes"], "secondary": ["hamstrings"]},
                {"name": "BSS", "sets": 4, "primary": ["quads", "glutes"]},
                {"name": "Abduction", "sets": 3, "primary": ["glutes"]}]},
            {"name": "Upper", "exercises": [
                {"name": "Incline Press", "sets": 3, "primary": ["chest"],
                 "secondary": ["triceps", "front delts"]},
                {"name": "OH Extension", "sets": 4, "primary": ["triceps"]}]},
        ],
        "targets": {"glutes": [12, 16], "triceps": [8, 12], "hamstrings": [10, 15]},
    }

    def test_counts(self):
        out = sc.run("sets", self.PLAN)
        rows = {r["muscle"]: r for r in out["muscles"]}
        self.assertEqual(rows["glutes"]["direct"], 11)
        self.assertEqual(rows["triceps"]["direct"], 4)
        self.assertEqual(rows["triceps"]["fractional"], 5.5)
        self.assertEqual(rows["triceps"]["nippard_count"], 4)
        self.assertEqual(rows["hamstrings"]["fractional"], 2)
        self.assertEqual(rows["hamstrings"]["status"], "below")
        self.assertEqual(rows["hamstrings"]["gap"], 8)
        self.assertEqual(rows["glutes"]["status"], "below")  # 11 < 12: never round a gap away
        self.assertEqual(out["weekly_sets"], 18)

    def test_per_session_cap_flag(self):
        plan = {"days": [{"name": "D", "exercises": [
            {"name": "A", "sets": 5, "primary": ["glutes"]},
            {"name": "B", "sets": 4, "primary": ["glutes"]}]}]}
        out = sc.run("sets", plan)
        self.assertEqual(out["days"][0]["muscles_over_8_direct_sets"], {"glutes": 9})

    def test_missing_primary(self):
        with self.assertRaises(sc.InputError):
            sc.run("sets", {"days": [{"exercises": [{"name": "X", "sets": 3}]}]})


class TestBudget(unittest.TestCase):
    def test_pace_and_skip(self):
        workouts = [
            wk("2026-10-20T18:00:00Z", "2026-10-20T19:12:00Z", sets=18),   # 4.0
            wk("2026-10-22T18:00:00Z", "2026-10-22T19:21:00Z", sets=18),   # 4.5
            wk("2026-10-24T18:00:00Z", "2026-10-24T23:50:00Z", sets=16),   # forgot to stop
        ]
        out = sc.run("budget", {"workouts": workouts, "session_minutes": 75, "exercise_cap": 6,
                                "plan": [{"name": "Upper A", "sets": 17, "exercises": 6},
                                         {"name": "Long", "sets": 20, "exercises": 7}]})
        self.assertEqual(out["pace_min_per_set"], 4.25)
        self.assertEqual(len(out["skipped"]), 1)
        self.assertEqual(out["sets_that_fit"], 17)
        self.assertTrue(out["plan"][0]["fits_time"])
        self.assertFalse(out["plan"][1]["fits_time"])
        self.assertFalse(out["plan"][1]["within_exercise_cap"])

    def test_counts_hevy_sets_without_warmups(self):
        ex = [{"title": "Squat", "sets": [{"type": "warmup"}, {"type": "normal"}, {"type": "normal"}]}]
        out = sc.run("budget", {"workouts": [wk("2026-10-20T18:00:00Z", "2026-10-20T18:10:00Z", ex)]})
        self.assertEqual(out["pace_min_per_set"], 5.0)

    def test_default_when_no_history(self):
        out = sc.run("budget", {"workouts": []})
        self.assertEqual(out["pace_min_per_set"], 4.0)
        self.assertIn("default", out["pace_source"])


class TestE1rm(unittest.TestCase):
    def test_values(self):
        out = sc.run("e1rm", {"weight_kg": 100, "reps": 5})
        self.assertEqual(out["epley"], 116.7)
        self.assertEqual(out["brzycki"], 112.5)

    def test_single_and_rir(self):
        self.assertEqual(sc.run("e1rm", {"weight_kg": 80, "reps": 1})["estimate"], 80)
        self.assertEqual(sc.run("e1rm", {"weight_kg": 60, "reps": 4, "rir": 2})["effective_reps"], 6)

    def test_high_rep_warning(self):
        self.assertIn("warning", sc.run("e1rm", {"weight_kg": 20, "reps": 15}))


def hevy_session(date, title, sets):
    return {"title": "S", "start_time": f"{date}T18:00:00Z", "end_time": f"{date}T19:00:00Z",
            "exercises": [{"title": title, "sets": sets}]}


def s(w, r, t="normal", rpe=None):
    return {"weight_kg": w, "reps": r, "type": t, "rpe": rpe}


class TestEvidence(unittest.TestCase):
    LOG = {"Hip Thrust (Barbell)": {"changed": "2026-11-05", "weight_kg": 105,
                                    "rep_range": [6, 10], "sets": 4}}

    def test_same_day_session_does_not_count(self):
        # The session that triggered the change is not new evidence.
        w = [hevy_session("2026-11-05", "Hip Thrust (Barbell)", [s(105, 10)] * 4)]
        r = sc.run("evidence", {"log": self.LOG, "workouts": w})["exercises"][0]
        self.assertEqual(r["verdict"], "no new data")
        self.assertEqual(r["next_weight_kg"], 105)

    def test_top_of_range_increases(self):
        w = [hevy_session("2026-11-07", "Hip Thrust (Barbell)",
                          [s(60, 8, "warmup")] + [s(105, 10)] * 4)]
        r = sc.run("evidence", {"log": self.LOG, "workouts": w})["exercises"][0]
        self.assertEqual(r["action"], "increase")
        self.assertEqual(r["next_weight_kg"], 107.5)

    def test_easy_top_of_range_doubles_jump(self):
        w = [hevy_session("2026-11-07", "Hip Thrust (Barbell)", [s(105, 10, rpe=7)] * 4)]
        r = sc.run("evidence", {"log": self.LOG, "workouts": w})["exercises"][0]
        self.assertEqual(r["next_weight_kg"], 110)
        self.assertEqual(r["rpe_avg"], 7)

    def test_hard_top_of_range_single_jump(self):
        w = [hevy_session("2026-11-07", "Hip Thrust (Barbell)", [s(105, 10, rpe=9)] * 4)]
        r = sc.run("evidence", {"log": self.LOG, "workouts": w})["exercises"][0]
        self.assertEqual(r["next_weight_kg"], 107.5)

    def test_within_range(self):
        w = [hevy_session("2026-11-07", "Hip Thrust (Barbell)", [s(105, 10), s(105, 9), s(105, 8), s(105, 8)])]
        r = sc.run("evidence", {"log": self.LOG, "workouts": w})["exercises"][0]
        self.assertEqual(r["action"], "add reps")

    def test_below_planned_weight(self):
        w = [hevy_session("2026-11-07", "Hip Thrust (Barbell)", [s(100, 10)] * 4)]
        r = sc.run("evidence", {"log": self.LOG, "workouts": w})["exercises"][0]
        self.assertEqual(r["verdict"], "below planned weight")

    def test_below_range(self):
        w = [hevy_session("2026-11-07", "Hip Thrust (Barbell)", [s(105, 7), s(105, 5)])]
        r = sc.run("evidence", {"log": self.LOG, "workouts": w})["exercises"][0]
        self.assertEqual(r["action"], "hold or reduce 5-10%")
        self.assertEqual(r["reduced_weight_kg"], 97.5)

    def test_stall(self):
        w = [hevy_session(d, "Hip Thrust (Barbell)", [s(105, 8)] * 4)
             for d in ("2026-11-07", "2026-11-14", "2026-11-21")]
        r = sc.run("evidence", {"log": self.LOG, "workouts": w})["exercises"][0]
        self.assertTrue(r.get("stall"))
        self.assertEqual(r["sessions_in_window"], 3)


class TestCli(unittest.TestCase):
    def run_cli(self, *args, stdin=None):
        return subprocess.run([sys.executable, str(ROOT / "tools" / "shifu_calc.py"), *args],
                              input=stdin, capture_output=True, text=True)

    def test_stdin_roundtrip(self):
        p = self.run_cli("e1rm", "-", stdin=json.dumps({"weight_kg": 60, "reps": 5}))
        self.assertEqual(p.returncode, 0)
        self.assertEqual(json.loads(p.stdout)["_tool"]["command"], "e1rm")

    def test_error_exit_code(self):
        p = self.run_cli("macros", "-", stdin="{}")
        self.assertEqual(p.returncode, 2)
        self.assertIn("error", json.loads(p.stdout))

    def test_skill_copies_match_source(self):
        src = (ROOT / "tools" / "shifu_calc.py").read_text()
        copies = list((ROOT / "skills").glob("*/scripts/shifu_calc.py"))
        self.assertTrue(copies, "run scripts/sync-knowledge.sh")
        for c in copies:
            self.assertEqual(c.read_text(), src, f"{c} is stale: run scripts/sync-knowledge.sh")


if __name__ == "__main__":
    unittest.main()
