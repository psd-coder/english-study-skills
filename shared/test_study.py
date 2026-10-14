import contextlib
import io
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import study

COACH_LOG = """English check

Old format message without sections.
  output your provided me -> output what you provided me
      Use relative pronouns

English check: all good

│ English check
│
│ Yours:
│ Lets' change references list for russian
│
│ Fixed:
│ Let's change the references list for Russian
│
│ 1. [spelling] Lets' -> Let's
│    Contraction of 'let us' is spelled with apostrophe before s.
│ 2. [article] change references list -> change the references list
│    Specific countable nouns need a definite article.
│ 3. [weird] for russian -> for Russian
│    Language names are capitalized.
│ 4. [article] in office -> in the office
╰─────
"""


class StudyTestCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name) / "study"
        self.env = mock.patch.dict(
            os.environ,
            {"ENGLISH_STUDY_DIR": str(self.dir), "ENGLISH_STUDY_TODAY": "2026-10-12"},
        )
        self.env.start()
        self.pointer = mock.patch.object(study, "POINTER_FILE", Path(self.tmp.name) / "location")
        self.pointer.start()
        self.run_cli("init", "--name", "Ann", "--l1", "Russian")

    def tearDown(self):
        self.env.stop()
        self.pointer.stop()
        self.tmp.cleanup()

    def set_today(self, day):
        os.environ["ENGLISH_STUDY_TODAY"] = day

    def run_cli(self, *argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            study.main(list(argv))
        text = out.getvalue().strip()
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return text


class InitAndSettingsTest(StudyTestCase):
    def test_init_creates_files_once(self):
        self.assertTrue((self.dir / "profile.md").exists())
        again = self.run_cli("init")
        self.assertEqual(again["created"], [])

    def test_init_with_explicit_dir_writes_pointer(self):
        other = Path(self.tmp.name) / "custom"
        self.run_cli("--dir", str(other), "init")
        self.assertEqual(study.POINTER_FILE.read_text().strip(), str(other))

    def test_status_before_init(self):
        other = Path(self.tmp.name) / "empty"
        result = self.run_cli("--dir", str(other), "status")
        self.assertFalse(result["initialized"])

    def test_set_updates_existing_key_and_adds_new_key(self):
        self.run_cli("set", "homework_new", "16")
        self.run_cli("set", "schedule", "manual")
        conf = study.settings(self.dir)
        self.assertEqual(conf["homework_new"], "16")
        self.assertEqual(conf["schedule"], "manual")
        self.assertEqual(conf["name"], "Ann")
        self.assertIn("## Preferences", (self.dir / "profile.md").read_text())

    def test_set_rejects_unknown_key(self):
        with self.assertRaises(SystemExit), contextlib.redirect_stdout(io.StringIO()):
            study.main(["set", "Preferences", "use IT examples"])
        self.assertNotIn("Preferences:", (self.dir / "profile.md").read_text())

    def test_l1_cue_share_follows_level_unless_fixed(self):
        self.assertEqual(study.l1_cue_share({"level_overall": "B2-low"}), 15)
        self.assertEqual(study.l1_cue_share({"level_vocabulary": "A2", "level_overall": "B1"}), 50)
        self.assertEqual(study.l1_cue_share({"level_overall": "C1"}), 5)
        self.assertEqual(study.l1_cue_share({}), 30)
        self.assertEqual(study.l1_cue_share({"l1_cue_share": "0", "level_overall": "A1"}), 0)


class StateTest(StudyTestCase):
    def test_state_update_and_stale_guard_within_one_second(self):
        rev = self.run_cli("status")["state"]["rev"]
        result = self.run_cli("state", "next_step=grade", "--expect", rev)
        self.assertEqual((result["next_step"], result["rev"]), ("grade", "1"))
        with self.assertRaises(SystemExit), contextlib.redirect_stdout(io.StringIO()):
            study.main(["state", "next_step=lesson", "--expect", rev])
        self.assertEqual(study.read_fields(self.dir / "state.md", "fields")["next_step"], "grade")

    def test_state_rejects_unknown_field(self):
        with self.assertRaises(SystemExit), contextlib.redirect_stdout(io.StringIO()):
            study.main(["state", "nextstep=grade"])

    def test_state_rejects_bad_pair(self):
        with self.assertRaises(SystemExit), contextlib.redirect_stdout(io.StringIO()):
            study.main(["state", "nonsense"])


class CardsTest(StudyTestCase):
    def add(self, front, kind="vocab"):
        return self.run_cli("card-add", "--kind", kind, "--front", front)["added"]["id"]

    def test_add_is_case_insensitive_dedup(self):
        self.add("make a decision")
        result = self.run_cli("card-add", "--kind", "vocab", "--front", "Make a Decision")
        self.assertIn("existing", result)

    def test_leitner_promotion_needs_separate_days(self):
        card = self.add("reckon")
        first = self.run_cli("card-grade", f"{card}+")["graded"][0]
        self.assertEqual((first["box"], first["due"]), (1, "2026-10-13"))
        same_day = self.run_cli("card-grade", f"{card}+")["graded"][0]
        self.assertIn("skipped", same_day)
        self.set_today("2026-10-13")
        second = self.run_cli("card-grade", f"{card}+")["graded"][0]
        self.assertEqual((second["box"], second["due"]), (2, "2026-10-16"))

    def test_failure_demotes_to_box_one(self):
        card = self.add("signpost")
        for day in ["2026-10-12", "2026-10-13", "2026-10-16"]:
            self.set_today(day)
            self.run_cli("card-grade", f"{card}+")
        self.set_today("2026-10-23")
        result = self.run_cli("card-grade", f"{card}-")["graded"][0]
        self.assertEqual((result["box"], result["due"]), (1, "2026-10-24"))

    def test_failure_on_new_card_keeps_it_new(self):
        card = self.add("dwell")
        result = self.run_cli("card-grade", f"{card}-")["graded"][0]
        self.assertEqual((result["box"], result["due"]), (0, "2026-10-13"))
        self.assertEqual(self.run_cli("cards")[0]["status"], "new")

    def test_coach_log_imported_as_jsonl_fails_cleanly(self):
        log = Path(self.tmp.name) / "coach.log"
        log.write_text(COACH_LOG)
        with self.assertRaises(SystemExit), contextlib.redirect_stdout(io.StringIO()):
            study.main(["import-stream", str(log)])

    def test_mastered_after_all_intervals(self):
        card = self.add("Present perfect", kind="grammar")
        day = study.dt.date(2026, 10, 12)
        for interval in [0] + study.INTERVALS:
            day += study.dt.timedelta(days=interval)
            self.set_today(day.isoformat())
            self.run_cli("card-grade", f"{card}+")
        cards = self.run_cli("cards", "--kind", "grammar")
        self.assertEqual(cards[0]["status"], "mastered")
        self.assertIsNone(cards[0]["due"])

    def test_due_filter_and_status_counts(self):
        a = self.add("dwell")
        self.add("nudge")
        self.run_cli("card-grade", f"{a}+")
        due = self.run_cli("cards", "--due")
        self.assertEqual([c["front"] for c in due], ["nudge"])
        status = self.run_cli("status")
        self.assertEqual(status["due"], {"vocab": 1})
        self.assertEqual(status["cards"]["vocab"], {"learning": 1, "new": 1})

    def test_grade_unknown_card_fails(self):
        with self.assertRaises(SystemExit), contextlib.redirect_stdout(io.StringIO()):
            study.main(["card-grade", "99+"])


class LogAndStatsTest(StudyTestCase):
    def test_sample_unknown_category_becomes_other(self):
        row = self.run_cli(
            "log", "sample", json.dumps({"words": 50, "errors": [{"category": "bad"}]})
        )["row"]
        self.assertEqual(row["errors"][0]["category"], "other")
        self.assertEqual(row["date"], "2026-10-12")

    def test_stats_rates_and_streak(self):
        for day in ["2026-10-08", "2026-10-09", "2026-10-12"]:
            self.run_cli("log", "session", json.dumps({"date": day, "minutes": 30}))
        self.run_cli(
            "log",
            "sample",
            json.dumps({"words": 200, "errors": [{"category": "article"}] * 4}),
        )
        self.run_cli("log", "sample", json.dumps({"words": None, "errors": [{}]}))
        stats = self.run_cli("stats", "--weeks", "2")
        this_week = stats["weeks"][-1]
        self.assertEqual(this_week["rate_per_100"], 2.0)
        self.assertEqual(this_week["category_rate_per_100"], {"article": 2.0})
        self.assertEqual(stats["streak"], 3)
        self.assertEqual(stats["total_minutes"], 90)

    def test_streak_skips_non_study_days_and_breaks_on_gap(self):
        self.run_cli("log", "session", json.dumps({"date": "2026-10-07", "minutes": 20}))
        self.run_cli("log", "session", json.dumps({"date": "2026-10-09", "minutes": 20}))
        self.assertEqual(self.run_cli("status")["streak"], 1)

    def test_episode_used(self):
        self.run_cli("log", "episode", json.dumps({"url": "https://example.com/ep1"}))
        self.assertTrue(self.run_cli("episode-used", "https://example.com/ep1")["used"])
        self.assertFalse(self.run_cli("episode-used", "https://example.com/ep2")["used"])

    def test_checkpoint_and_plan_week(self):
        self.run_cli("set", "plan_start", "2026-09-28")
        self.run_cli("set", "next_checkpoint", "2026-10-12")
        self.run_cli("log", "assessment", json.dumps({"kind": "placement", "date": "2026-09-28"}))
        self.run_cli("log", "assessment", json.dumps({"kind": "confirm", "overall": "B1"}))
        status = self.run_cli("status")
        self.assertEqual(status["placed_on"], "2026-09-28")
        self.assertEqual(status["last_assessment"]["kind"], "confirm")
        self.assertEqual(status["plan_week"], 3)
        self.assertTrue(status["checkpoint_due"])

    def test_dashboard_renders(self):
        self.run_cli("log", "assessment", json.dumps({"kind": "placement", "overall": "B1"}))
        path = Path(self.run_cli("dashboard")["path"])
        page = path.read_text()
        self.assertIn("English progress - Ann", page)
        self.assertIn("placement", page)


class StreamTest(StudyTestCase):
    def test_parse_coach_log(self):
        entries = study.parse_coach_log(COACH_LOG)
        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[0], {"words": None, "errors": []})
        self.assertEqual(entries[1]["words"], 6)
        categories = [e["category"] for e in entries[1]["errors"]]
        self.assertEqual(categories, ["spelling", "article", "other", "article"])
        self.assertNotIn("rule", entries[1]["errors"][3])
        self.assertEqual(entries[1]["errors"][1]["right"], "change the references list")
        self.assertTrue(entries[1]["errors"][0]["rule"].startswith("Contraction"))

    def test_import_is_incremental(self):
        log = Path(self.tmp.name) / "coach.log"
        log.write_text(COACH_LOG)
        first = self.run_cli("import-stream", str(log), "--format", "coach", "--name", "coach")
        self.assertEqual(first["streams"], [{"stream": "coach", "imported": 2}])
        again = self.run_cli("import-stream")
        self.assertEqual(again["streams"], [{"stream": "coach", "imported": 0}])
        with open(log, "a") as f:
            f.write("English check: all good\n")
        third = self.run_cli("import-stream")
        self.assertEqual(third["streams"], [{"stream": "coach", "imported": 1}])
        log.unlink()
        self.assertIn("missing", self.run_cli("import-stream")["streams"][0])

    def test_import_jsonl(self):
        stream = Path(self.tmp.name) / "errors.jsonl"
        stream.write_text(
            json.dumps({"date": "2026-10-10", "words": 30, "errors": [{"category": "tense"}]})
            + "\n"
            + '{"words": 10, "err'
        )
        result = self.run_cli("import-stream", str(stream), "--name", "mine")
        self.assertEqual(result["streams"][0]["imported"], 1)
        samples = study.read_jsonl(self.dir, "samples")
        self.assertEqual(samples[0]["source"], "stream:mine")

    def test_stream_samples_have_their_own_rate(self):
        self.run_cli("log", "sample", json.dumps({"words": 100, "errors": [{"category": "tense"}]}))
        self.run_cli(
            "log",
            "sample",
            json.dumps({"source": "stream:coach", "words": 50, "errors": [{}, {}]}),
        )
        weeks = self.run_cli("stats", "--weeks", "2")["weeks"]
        self.assertEqual(set(weeks[0]), set(weeks[1]))
        week = weeks[1]
        self.assertEqual(week["rate_per_100"], 1.0)
        self.assertEqual(week["stream_rate_per_100"], 4.0)

    def test_import_missing_file_fails(self):
        with self.assertRaises(SystemExit), contextlib.redirect_stdout(io.StringIO()):
            study.main(["import-stream", "/no/such/file"])


if __name__ == "__main__":
    unittest.main()
