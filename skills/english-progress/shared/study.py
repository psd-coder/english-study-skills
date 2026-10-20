#!/usr/bin/env python3
"""Data helper for the english-study skills. Python 3.8+, standard library only.

Run `study.py --help` for commands. Every command prints JSON or a plain path, so an
agent can read the result directly.
"""

import argparse
import datetime as dt
import html
import json
import os
import re
import sys
from pathlib import Path

DEFAULT_DIR = Path.home() / ".english-study"
POINTER_FILE = Path.home() / ".config" / "english-study" / "location"
INTERVALS = [1, 3, 7, 21, 60]
MASTERED_BOX = len(INTERVALS) + 1
CATEGORIES = [
    "article",
    "tense",
    "preposition",
    "wordorder",
    "agreement",
    "collocation",
    "phrasal",
    "countability",
    "spelling",
    "capitalization",
    "vocabulary",
    "modal",
    "verbpattern",
    "other",
]
L1_CUE_SHARE = {"A1": 50, "A2": 50, "B1": 30, "B2": 15, "C1": 5, "C2": 0}
SETTINGS_KEYS = [
    "name",
    "l1",
    "minutes_per_day",
    "days",
    "homework_new",
    "homework_review",
    "new_chunks_per_day",
    "l1_cue_share",
    "focus",
    "weight_input",
    "weight_output",
    "weight_language",
    "weight_fluency",
    "level_overall",
    "level_grammar",
    "level_vocabulary",
    "level_reading",
    "level_listening",
    "level_speaking",
    "level_writing",
    "level_status",
    "goal",
    "deadline",
    "plan_start",
    "checkpoint_weeks",
    "next_checkpoint",
    "transcriber",
    "schedule",
]
STATE_KEYS = [
    "next_step",
    "open_homework",
    "homework_date",
    "unanswered_runs",
    "paused",
    "assessment_progress",
    "week_planned",
]
WEEKDAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
JSONL_FILES = ["cards", "sessions", "samples", "assessments", "episodes"]

PROFILE_TEMPLATE = """# English study profile

## Settings
name: {name}
l1: {l1}
minutes_per_day: 30
days: mon,tue,wed,thu,fri
homework_new: 12
homework_review: 4
new_chunks_per_day: 6
l1_cue_share: auto
focus:
weight_input: 25
weight_output: 25
weight_language: 25
weight_fluency: 25
level_overall:
level_grammar:
level_vocabulary:
level_reading:
level_listening:
level_speaking:
level_writing:
level_status: none
goal:
deadline:
plan_start:
checkpoint_weeks: 6
next_checkpoint:
transcriber: handy-parakeet
schedule: none

## Preferences

## Notes
"""

STATE_TEMPLATE = """# State

## Fields
rev: 0
updated: {now}
next_step: assessment
open_homework: none
homework_date: none
unanswered_runs: 0
paused: no
assessment_progress: none
week_planned: 0

## Notes
"""

PLAN_TEMPLATE = """# Study plan

The plan is written by english-planner after the first assessment.
"""


def today():
    override = os.environ.get("ENGLISH_STUDY_TODAY")
    return dt.date.fromisoformat(override) if override else dt.date.today()


def now_iso():
    return dt.datetime.now().replace(microsecond=0).isoformat()


def resolve_dir(explicit=None):
    if explicit:
        return Path(explicit).expanduser()
    env = os.environ.get("ENGLISH_STUDY_DIR")
    if env:
        return Path(env).expanduser()
    if POINTER_FILE.exists():
        location = POINTER_FILE.read_text().strip()
        if location:
            return Path(location).expanduser()
    return DEFAULT_DIR


def fail(message):
    print(json.dumps({"error": message}))
    sys.exit(1)


def require_dir(data_dir):
    if not (data_dir / "profile.md").exists():
        fail(f"No study folder at {data_dir}. Run the english-assessment skill to set it up.")


def read_jsonl(data_dir, name):
    path = data_dir / f"{name}.jsonl"
    if not path.exists():
        return []
    rows = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def write_jsonl(data_dir, name, rows):
    path = data_dir / f"{name}.jsonl"
    tmp = path.with_suffix(".jsonl.tmp")
    tmp.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows))
    os.replace(tmp, path)


def append_jsonl(data_dir, name, row):
    with open(data_dir / f"{name}.jsonl", "a") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def read_fields(path, section):
    fields = {}
    inside = False
    for line in path.read_text().splitlines():
        if line.startswith("## "):
            inside = line[3:].strip().lower() == section
            continue
        if inside and ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()
    return fields


def write_field(path, section, key, value):
    lines = path.read_text().splitlines()
    inside = False
    section_end = None
    for i, line in enumerate(lines):
        if line.startswith("## "):
            if inside:
                section_end = i
                break
            inside = line[3:].strip().lower() == section
            continue
        if inside and ":" in line and line.split(":", 1)[0].strip() == key:
            lines[i] = f"{key}: {value}"
            path.write_text("\n".join(lines) + "\n")
            return
    if not inside and section_end is None:
        fail(f"Section '## {section}' not found in {path.name}")
    insert_at = section_end if section_end is not None else len(lines)
    while insert_at > 0 and not lines[insert_at - 1].strip():
        insert_at -= 1
    lines.insert(insert_at, f"{key}: {value}")
    path.write_text("\n".join(lines) + "\n")


def append_note(path, text):
    lines = path.read_text().splitlines()
    start = next((i for i, line in enumerate(lines) if line.strip().lower() == "## notes"), None)
    if start is None:
        fail(f"Section '## Notes' not found in {path.name}")
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    while end > start + 1 and not lines[end - 1].strip():
        end -= 1
    lines.insert(end, text)
    path.write_text("\n".join(lines) + "\n")


def settings(data_dir):
    return read_fields(data_dir / "profile.md", "settings")


def base_level(level):
    match = re.match(r"([ABC][12])", (level or "").upper())
    return match.group(1) if match else None


def l1_cue_share(conf):
    value = conf.get("l1_cue_share", "auto")
    if value.isdigit():
        return int(value)
    level = base_level(conf.get("level_vocabulary")) or base_level(conf.get("level_overall"))
    return L1_CUE_SHARE.get(level, 30)


def card_status(card):
    box = card["box"]
    if box == 0:
        return "new"
    if box <= 2:
        return "learning"
    if box < MASTERED_BOX:
        return "reviewing"
    return "mastered"


def is_due(card, on):
    return card.get("due") is not None and dt.date.fromisoformat(card["due"]) <= on


def study_days(conf):
    days = [d.strip().lower()[:3] for d in conf.get("days", "").split(",") if d.strip()]
    return [d for d in days if d in WEEKDAYS] or WEEKDAYS[:5]


def streak(sessions, conf, on):
    dates = {dt.date.fromisoformat(s["date"]) for s in sessions}
    days = study_days(conf)
    count = 0
    cursor = on
    if cursor not in dates:
        cursor -= dt.timedelta(days=1)
    for _ in range(3650):
        if WEEKDAYS[cursor.weekday()] in days:
            if cursor not in dates:
                break
            count += 1
        cursor -= dt.timedelta(days=1)
    return count


def cmd_where(args):
    print(resolve_dir(args.dir))


def cmd_init(args):
    data_dir = resolve_dir(args.dir)
    data_dir.mkdir(parents=True, exist_ok=True)
    (data_dir / "homework").mkdir(exist_ok=True)
    (data_dir / "inbox").mkdir(exist_ok=True)
    created = []
    templates = {
        "profile.md": PROFILE_TEMPLATE.format(name=args.name or "", l1=args.l1 or ""),
        "state.md": STATE_TEMPLATE.format(now=now_iso()),
        "plan.md": PLAN_TEMPLATE,
    }
    for name, content in templates.items():
        path = data_dir / name
        if not path.exists():
            path.write_text(content)
            created.append(name)
    for name in JSONL_FILES:
        path = data_dir / f"{name}.jsonl"
        if not path.exists():
            path.touch()
            created.append(path.name)
    if args.dir and data_dir.resolve() != DEFAULT_DIR.resolve():
        POINTER_FILE.parent.mkdir(parents=True, exist_ok=True)
        POINTER_FILE.write_text(str(data_dir) + "\n")
    print(json.dumps({"data_dir": str(data_dir), "created": created}))


def cmd_set(args):
    data_dir = resolve_dir(args.dir)
    require_dir(data_dir)
    if args.key not in SETTINGS_KEYS:
        fail(
            f"Unknown setting '{args.key}'. Known settings: {', '.join(SETTINGS_KEYS)}. "
            "Personal rules go as a line under '## Preferences' in profile.md."
        )
    write_field(data_dir / "profile.md", "settings", args.key, args.value)
    print(json.dumps({"set": {args.key: args.value}}))


def cmd_note(args):
    data_dir = resolve_dir(args.dir)
    require_dir(data_dir)
    text = " ".join(args.text.split())
    if not text:
        fail("Note text is empty")
    append_note(data_dir / "profile.md", text)
    print(json.dumps({"noted": text}, ensure_ascii=False))


def cmd_state(args):
    data_dir = resolve_dir(args.dir)
    require_dir(data_dir)
    path = data_dir / "state.md"
    current = read_fields(path, "fields")
    rev = int(current.get("rev") or 0)
    if args.expect is not None and str(rev) != args.expect:
        fail(
            "state.md changed since you read it (another session wrote it). "
            "Run `status` again and rebuild your step on the new state."
        )
    pairs = []
    for pair in args.pairs:
        if "=" not in pair:
            fail(f"Expected key=value, got '{pair}'")
        key, value = (part.strip() for part in pair.split("=", 1))
        if key not in STATE_KEYS:
            fail(f"Unknown state field '{key}'. Known fields: {', '.join(STATE_KEYS)}")
        pairs.append((key, value))
    for key, value in pairs:
        write_field(path, "fields", key, value)
    write_field(path, "fields", "rev", str(rev + 1))
    write_field(path, "fields", "updated", now_iso())
    print(json.dumps(read_fields(path, "fields")))


def cmd_status(args):
    data_dir = resolve_dir(args.dir)
    if not (data_dir / "profile.md").exists():
        print(json.dumps({"data_dir": str(data_dir), "initialized": False}))
        return
    on = today()
    conf = settings(data_dir)
    cards = read_jsonl(data_dir, "cards")
    sessions = read_jsonl(data_dir, "sessions")
    assessments = read_jsonl(data_dir, "assessments")
    counts = {}
    due = {}
    for card in cards:
        kind_counts = counts.setdefault(card["kind"], {})
        status = card_status(card)
        kind_counts[status] = kind_counts.get(status, 0) + 1
        if is_due(card, on):
            due[card["kind"]] = due.get(card["kind"], 0) + 1
    last = sessions[-1] if sessions else None
    plan_week = None
    if conf.get("plan_start"):
        start = dt.date.fromisoformat(conf["plan_start"])
        plan_week = (on - start).days // 7 + 1
    checkpoint_due = bool(
        conf.get("next_checkpoint") and dt.date.fromisoformat(conf["next_checkpoint"]) <= on
    )
    print(
        json.dumps(
            {
                "data_dir": str(data_dir),
                "initialized": True,
                "today": on.isoformat(),
                "weekday": WEEKDAYS[on.weekday()],
                "study_day": WEEKDAYS[on.weekday()] in study_days(conf),
                "settings": conf,
                "l1_cue_share": l1_cue_share(conf),
                "state": read_fields(data_dir / "state.md", "fields"),
                "assessed": bool(assessments),
                "last_assessment": (
                    {k: assessments[-1].get(k) for k in ("date", "kind", "overall")}
                    if assessments
                    else None
                ),
                "placed_on": next(
                    (a.get("date") for a in reversed(assessments) if a.get("kind") == "placement"),
                    None,
                ),
                "plan_week": plan_week,
                "checkpoint_due": checkpoint_due,
                "due": due,
                "cards": counts,
                "last_session": last,
                "days_since_last_session": (
                    (on - dt.date.fromisoformat(last["date"])).days if last else None
                ),
                "streak": streak(sessions, conf, on),
            },
            ensure_ascii=False,
        )
    )


def cmd_card_add(args):
    data_dir = resolve_dir(args.dir)
    require_dir(data_dir)
    cards = read_jsonl(data_dir, "cards")
    key = args.front.strip().lower()
    for card in cards:
        if card["kind"] == args.kind and card["front"].strip().lower() == key:
            print(json.dumps({"existing": card}, ensure_ascii=False))
            return
    data = json.loads(args.data) if args.data else {}
    on = today()
    card = {
        "id": max((c["id"] for c in cards), default=0) + 1,
        "kind": args.kind,
        "front": args.front.strip(),
        "data": data,
        "box": 0,
        "due": on.isoformat(),
        "created": on.isoformat(),
        "history": [],
    }
    append_jsonl(data_dir, "cards", card)
    print(json.dumps({"added": card}, ensure_ascii=False))


def grade_card(card, ok, cue, on):
    card["history"].append({"date": on.isoformat(), "ok": ok, "cue": cue})
    if ok:
        card["box"] = min(card["box"] + 1, MASTERED_BOX)
    else:
        card["box"] = 0 if card["box"] == 0 else 1
    if card["box"] == MASTERED_BOX:
        card["due"] = None
    else:
        card["due"] = (on + dt.timedelta(days=INTERVALS[max(card["box"], 1) - 1])).isoformat()
    return card


def cmd_card_grade(args):
    data_dir = resolve_dir(args.dir)
    require_dir(data_dir)
    cards = read_jsonl(data_dir, "cards")
    on = today()
    results = []
    by_id = {card["id"]: card for card in cards}
    for item in args.results:
        match = re.fullmatch(r"(\d+)([+-])", item)
        if not match:
            fail(f"Expected <id>+ or <id>-, got '{item}'")
        card = by_id.get(int(match.group(1)))
        if card is None:
            fail(f"No card with id {match.group(1)}")
        already = any(h["date"] == on.isoformat() for h in card["history"])
        if already and match.group(2) == "+":
            results.append({"id": card["id"], "skipped": "already graded today"})
            continue
        grade_card(card, match.group(2) == "+", args.cue, on)
        results.append({"id": card["id"], "box": card["box"], "due": card["due"]})
    write_jsonl(data_dir, "cards", cards)
    print(json.dumps({"graded": results}))


def cmd_cards(args):
    data_dir = resolve_dir(args.dir)
    require_dir(data_dir)
    on = today()
    rows = []
    for card in read_jsonl(data_dir, "cards"):
        if args.kind and card["kind"] != args.kind:
            continue
        if args.due and not is_due(card, on):
            continue
        if args.status and card_status(card) != args.status:
            continue
        if args.find and args.find.lower() not in card["front"].lower():
            continue
        rows.append({**card, "status": card_status(card)})
    rows.sort(key=lambda c: (c["due"] or "9999", c["box"], c["id"]))
    if args.limit:
        rows = rows[: args.limit]
    print(json.dumps(rows, ensure_ascii=False))


def cmd_log(args):
    data_dir = resolve_dir(args.dir)
    require_dir(data_dir)
    row = json.loads(args.json)
    row.setdefault("date", today().isoformat())
    if args.kind == "sample":
        for error in row.get("errors", []):
            if error.get("category") not in CATEGORIES:
                error["category"] = "other"
        row.setdefault("source", "lesson")
    append_jsonl(data_dir, f"{args.kind}s", row)
    print(json.dumps({"logged": args.kind, "row": row}, ensure_ascii=False))


def cmd_episode_used(args):
    data_dir = resolve_dir(args.dir)
    require_dir(data_dir)
    used = any(e.get("url") == args.url for e in read_jsonl(data_dir, "episodes"))
    print(json.dumps({"used": used}))


def week_start(day):
    return day - dt.timedelta(days=day.weekday())


def compute_stats(data_dir, weeks):
    on = today()
    first_week = week_start(on) - dt.timedelta(weeks=weeks - 1)
    buckets = {}
    for i in range(weeks):
        start = first_week + dt.timedelta(weeks=i)
        buckets[start] = {
            "week": start.isoformat(),
            "sessions": 0,
            "minutes": 0,
            "words": 0,
            "errors": 0,
            "by_category": {},
            "stream_words": 0,
            "stream_errors": 0,
        }
    for session in read_jsonl(data_dir, "sessions"):
        bucket = buckets.get(week_start(dt.date.fromisoformat(session["date"])))
        if bucket:
            bucket["sessions"] += 1
            bucket["minutes"] += int(session.get("minutes") or 0)
    for sample in read_jsonl(data_dir, "samples"):
        if not sample.get("words"):
            continue
        bucket = buckets.get(week_start(dt.date.fromisoformat(sample["date"])))
        if not bucket:
            continue
        if str(sample.get("source", "")).startswith("stream:"):
            bucket["stream_words"] += int(sample["words"])
            bucket["stream_errors"] += len(sample.get("errors", []))
            continue
        bucket["words"] += int(sample["words"])
        for error in sample.get("errors", []):
            bucket["errors"] += 1
            category = error.get("category", "other")
            bucket["by_category"][category] = bucket["by_category"].get(category, 0) + 1
    rows = []
    for bucket in buckets.values():
        words = bucket["words"]
        bucket["rate_per_100"] = round(bucket["errors"] * 100 / words, 2) if words else None
        bucket["category_rate_per_100"] = {
            category: round(count * 100 / words, 2)
            for category, count in sorted(bucket["by_category"].items(), key=lambda kv: -kv[1])
        }
        stream_words = bucket.pop("stream_words")
        stream_errors = bucket.pop("stream_errors")
        bucket["stream_rate_per_100"] = (
            round(stream_errors * 100 / stream_words, 2) if stream_words else None
        )
        del bucket["by_category"]
        rows.append(bucket)
    sessions = read_jsonl(data_dir, "sessions")
    return {
        "weeks": rows,
        "total_minutes": sum(int(s.get("minutes") or 0) for s in sessions),
        "total_sessions": len(sessions),
        "streak": streak(sessions, settings(data_dir), on),
    }


def cmd_stats(args):
    data_dir = resolve_dir(args.dir)
    require_dir(data_dir)
    print(json.dumps(compute_stats(data_dir, args.weeks), ensure_ascii=False))


def parse_coach_log(text):
    entries = []
    for block in re.split(r"^\S*\s*English check", text, flags=re.M)[1:]:
        lines = [re.sub(r"^│ ?", "", line) for line in block.splitlines()]
        head = lines[0].strip() if lines else ""
        if head.startswith(": all good") or head.startswith("all good"):
            entries.append({"words": None, "errors": []})
            continue
        if "Yours:" not in [line.strip() for line in lines]:
            continue
        yours = []
        errors = []
        mode = None
        last_error = None
        for line in lines[1:]:
            stripped = line.strip()
            if stripped.startswith(("╰", "╭", "─")):
                continue
            if stripped == "Yours:":
                mode = "yours"
                continue
            if stripped == "Fixed:":
                mode = "fixed"
                continue
            match = re.match(r"\d+\.\s+\[(\w+)\]\s+(.*?)\s+->\s+(.*)$", stripped)
            if match:
                mode = "errors"
                category = match.group(1) if match.group(1) in CATEGORIES else "other"
                last_error = {
                    "category": category,
                    "wrong": match.group(2),
                    "right": match.group(3),
                }
                errors.append(last_error)
                continue
            if mode == "yours" and stripped:
                yours.append(stripped)
            elif mode == "errors" and stripped and last_error and "rule" not in last_error:
                last_error["rule"] = stripped
        text_words = len(" ".join(yours).split())
        entries.append({"words": text_words or None, "errors": errors})
    return entries


def import_one(data_dir, cursors, source, fmt, name):
    key = str(source.resolve())
    offset = cursors.get(key, {}).get("offset", 0)
    raw = source.read_bytes()
    if offset > len(raw):
        offset = 0
    chunk = raw[offset:].decode("utf-8", errors="replace")
    complete = chunk[: chunk.rfind("\n") + 1]
    on = today().isoformat()
    imported = 0
    if fmt == "coach":
        for entry in parse_coach_log(complete):
            append_jsonl(data_dir, "samples", {"date": on, "source": f"stream:{name}", **entry})
            imported += 1
    else:
        for line in complete.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                fail(f"{source.name} has a non-JSON line; for a coach log use --format coach")
            for error in row.get("errors", []):
                if error.get("category") not in CATEGORIES:
                    error["category"] = "other"
            row.setdefault("date", on)
            row["source"] = f"stream:{name}"
            append_jsonl(data_dir, "samples", row)
            imported += 1
    consumed = len(complete.encode("utf-8"))
    cursors[key] = {"name": name, "format": fmt, "offset": offset + consumed}
    return imported


def cmd_import_stream(args):
    data_dir = resolve_dir(args.dir)
    require_dir(data_dir)
    cursors_path = data_dir / "streams.json"
    cursors = json.loads(cursors_path.read_text()) if cursors_path.exists() else {}
    results = []
    if args.path:
        source = Path(args.path).expanduser()
        if not source.exists():
            fail(f"No file at {source}")
        name = args.name or source.stem
        results.append({"stream": name, "imported": import_one(
            data_dir, cursors, source, args.format, name
        )})
    else:
        for key, stream in cursors.items():
            source = Path(key)
            if not source.exists():
                results.append({"stream": stream["name"], "missing": key})
                continue
            results.append({"stream": stream["name"], "imported": import_one(
                data_dir, cursors, source, stream["format"], stream["name"]
            )})
    cursors_path.write_text(json.dumps(cursors, indent=2) + "\n")
    print(json.dumps({"streams": results}))


def svg_line_chart(points, label):
    width, height, pad = 640, 220, 36
    values = [v for _, v in points if v is not None]
    if len(values) < 2:
        return '<p class="muted">Not enough data yet. The chart appears after two weeks.</p>'
    top = max(values) * 1.15 or 1
    step = (width - 2 * pad) / max(len(points) - 1, 1)

    def xy(i, v):
        return pad + i * step, height - pad - (v / top) * (height - 2 * pad)

    path = []
    dots = []
    for i, (week, v) in enumerate(points):
        if v is None:
            continue
        x, y = xy(i, v)
        path.append(f"{'M' if not path else 'L'}{x:.1f},{y:.1f}")
        dots.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" class="dot">'
            f"<title>Week of {week}: {v} {html.escape(label)}</title></circle>"
        )
    first, last = points[0][0], points[-1][0]
    return (
        f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="{html.escape(label)}">'
        f'<line x1="{pad}" y1="{height - pad}" x2="{width - pad}" y2="{height - pad}"'
        ' class="axis"/>'
        f'<text x="{pad}" y="{height - 10}" class="tick">{first}</text>'
        f'<text x="{width - pad}" y="{height - 10}" class="tick" text-anchor="end">{last}</text>'
        f'<text x="{pad}" y="{pad - 12}" class="tick">max {top / 1.15:.1f}</text>'
        f'<path d="{" ".join(path)}" class="line"/>{"".join(dots)}</svg>'
    )


def table(headers, rows):
    head = "".join(f"<th>{html.escape(h)}</th>" for h in headers)
    body = "".join(
        "<tr>" + "".join(f"<td>{html.escape(str(c))}</td>" for c in row) + "</tr>" for row in rows
    )
    return f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>"


DASHBOARD_CSS = """
:root{--bg:#fafaf7;--surface:#fff;--ink:#1d1d1b;--muted:#6b6b66;--line:#e4e2dc;--accent:#2f6fdb}
@media (prefers-color-scheme: dark){:root{--bg:#141413;--surface:#1f1f1d;--ink:#ecebe6;
--muted:#9c9b95;--line:#34332f;--accent:#7aa7f0}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);
font:16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
main{max-width:960px;margin:0 auto;padding:24px 16px 48px}h1{font-size:28px;margin:0 0 4px}
h2{font-size:18px;margin:32px 0 12px}.muted{color:var(--muted)}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;
margin-top:20px}
.tile{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:14px 16px}
.tile b{display:block;font-size:26px;line-height:1.2}.tile span{color:var(--muted);font-size:14px}
.card{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:16px;
overflow-x:auto}
table{border-collapse:collapse;width:100%;font-size:14px}th,td{text-align:left;padding:6px 8px;
border-bottom:1px solid var(--line)}th{color:var(--muted);font-weight:600}
svg{width:100%;height:auto}.axis{stroke:var(--line);stroke-width:1}.line{fill:none;
stroke:var(--accent);stroke-width:2}.dot{fill:var(--accent);stroke:var(--surface);stroke-width:2}
.tick{fill:var(--muted);font-size:12px}
"""


def cmd_dashboard(args):
    data_dir = resolve_dir(args.dir)
    require_dir(data_dir)
    conf = settings(data_dir)
    stats = compute_stats(data_dir, 12)
    on = today()
    cards = read_jsonl(data_dir, "cards")
    assessments = read_jsonl(data_dir, "assessments")
    due_now = sum(1 for c in cards if is_due(c, on))
    this_week = stats["weeks"][-1]
    tiles = [
        (stats["streak"], "study days in a row"),
        (f"{stats['total_minutes'] / 60:.1f}", "hours in total"),
        (this_week["sessions"], "sessions this week"),
        (due_now, "reviews due today"),
        (conf.get("level_overall") or "-", f"level ({conf.get('level_status', 'none')})"),
        (conf.get("next_checkpoint") or "-", "next checkpoint"),
    ]
    tiles_html = "".join(f'<div class="tile"><b>{html.escape(str(v))}</b><span>{l}</span></div>'
                         for v, l in tiles)
    rate_points = [(w["week"], w["rate_per_100"]) for w in stats["weeks"]]
    recent = stats["weeks"][-4:]
    earlier = stats["weeks"][-8:-4]

    def category_rates(weeks):
        words = sum(w["words"] for w in weeks)
        totals = {}
        for w in weeks:
            for category, rate in w["category_rate_per_100"].items():
                totals[category] = totals.get(category, 0) + rate * w["words"] / 100
        return {c: round(n * 100 / words, 2) for c, n in totals.items()} if words else {}

    now_rates = category_rates(recent)
    before_rates = category_rates(earlier)
    category_rows = [
        (c, before_rates.get(c, "-"), now_rates.get(c, "-"))
        for c in sorted(set(now_rates) | set(before_rates), key=lambda c: -now_rates.get(c, 0))
    ]
    level_rows = [
        (
            a.get("date"),
            a.get("kind", ""),
            a.get("overall", ""),
            ", ".join(f"{k} {v}" for k, v in (a.get("levels") or {}).items()),
        )
        for a in reversed(assessments)
    ]
    status_rows = []
    for kind in ("vocab", "grammar"):
        group = [c for c in cards if c["kind"] == kind]
        counts = {s: sum(1 for c in group if card_status(c) == s) for s in
                  ("new", "learning", "reviewing", "mastered")}
        status_rows.append((kind, *counts.values()))
    grammar_rows = [
        (c["front"], card_status(c), c["due"] or "-")
        for c in sorted((c for c in cards if c["kind"] == "grammar"), key=lambda c: c["id"])
    ]
    stream_points = [(w["week"], w["stream_rate_per_100"]) for w in stats["weeks"]]
    stream_section = (
        "<h2>Errors per 100 words in connected streams</h2>"
        f'<div class="card">{svg_line_chart(stream_points, "errors per 100 words (streams)")}</div>'
        if any(v is not None for _, v in stream_points)
        else ""
    )
    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>English Progress</title><style>{DASHBOARD_CSS}</style></head><body><main>
<h1>English progress{(" - " + html.escape(conf["name"])) if conf.get("name") else ""}</h1>
<p class="muted">Updated {on.isoformat()}. Goal: {html.escape(conf.get("goal") or "not set")}</p>
<div class="tiles">{tiles_html}</div>
<h2>Errors per 100 words, by week</h2>
<div class="card">{svg_line_chart(rate_points, "errors per 100 words")}</div>
{stream_section}
<h2>Errors per 100 words, by type</h2>
<div class="card">{table(["Type", "4 weeks before", "Last 4 weeks"], category_rows)
    if category_rows else '<p class="muted">No checked writing or speaking yet.</p>'}</div>
<h2>Level history</h2>
<div class="card">{table(["Date", "Kind", "Overall", "By skill"], level_rows)
    if level_rows else '<p class="muted">No assessment yet.</p>'}</div>
<h2>Review cards</h2>
<div class="card">{table(["Kind", "New", "Learning", "Reviewing", "Mastered"], status_rows)}</div>
<h2>Grammar topics</h2>
<div class="card">{table(["Topic", "Stage", "Next check"], grammar_rows)
    if grammar_rows else '<p class="muted">No grammar topics yet.</p>'}</div>
</main></body></html>
"""
    path = data_dir / "progress.html"
    path.write_text(page)
    print(json.dumps({"path": str(path)}))


def build_parser():
    parser = argparse.ArgumentParser(prog="study.py", description=__doc__.splitlines()[0])
    parser.add_argument("--dir", help="study folder (default: resolved from config)")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("where", help="print the study folder path").set_defaults(func=cmd_where)

    p = sub.add_parser("init", help="create the study folder")
    p.add_argument("--name")
    p.add_argument("--l1")
    p.set_defaults(func=cmd_init)

    sub.add_parser("status", help="everything a session needs, as JSON").set_defaults(
        func=cmd_status
    )

    p = sub.add_parser("set", help="change one setting in profile.md")
    p.add_argument("key")
    p.add_argument("value")
    p.set_defaults(func=cmd_set)

    p = sub.add_parser("note", help="add a line to ## Notes in profile.md")
    p.add_argument("text")
    p.set_defaults(func=cmd_note)

    p = sub.add_parser("state", help="update state.md fields: key=value ...")
    p.add_argument("pairs", nargs="+")
    p.add_argument("--expect", help="the 'rev' value you read; refuses if it changed")
    p.set_defaults(func=cmd_state)

    p = sub.add_parser("card-add", help="add a review card")
    p.add_argument("--kind", choices=["vocab", "grammar"], required=True)
    p.add_argument("--front", required=True, help="the chunk or the grammar topic")
    p.add_argument("--data", help="JSON object with details")
    p.set_defaults(func=cmd_card_add)

    p = sub.add_parser("card-grade", help="grade cards: 12+ (correct, unaided) 13- (wrong)")
    p.add_argument("results", nargs="+")
    p.add_argument("--cue", choices=["context", "l1", "free"], default="context")
    p.set_defaults(func=cmd_card_grade)

    p = sub.add_parser("cards", help="list cards")
    p.add_argument("--kind", choices=["vocab", "grammar"])
    p.add_argument("--status", choices=["new", "learning", "reviewing", "mastered"])
    p.add_argument("--due", action="store_true")
    p.add_argument("--find")
    p.add_argument("--limit", type=int)
    p.set_defaults(func=cmd_cards)

    p = sub.add_parser("log", help="append a record")
    p.add_argument("kind", choices=["session", "sample", "assessment", "episode"])
    p.add_argument("json")
    p.set_defaults(func=cmd_log)

    p = sub.add_parser("episode-used", help="check if a listening episode was used")
    p.add_argument("url")
    p.set_defaults(func=cmd_episode_used)

    p = sub.add_parser("stats", help="weekly totals and error rates")
    p.add_argument("--weeks", type=int, default=8)
    p.set_defaults(func=cmd_stats)

    sub.add_parser("dashboard", help="write progress.html").set_defaults(func=cmd_dashboard)

    p = sub.add_parser(
        "import-stream", help="connect and import an error stream; no path refreshes all streams"
    )
    p.add_argument("path", nargs="?")
    p.add_argument("--format", choices=["coach", "jsonl"], default="jsonl")
    p.add_argument("--name")
    p.set_defaults(func=cmd_import_stream)
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
