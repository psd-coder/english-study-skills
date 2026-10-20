---
name: today
description: Daily English lesson. Use when a scheduled English study run starts, or the learner says "next lesson", "let's study English", "resume", or sends answers to English homework.
license: MIT
---

# English today

The one entry point for every study day. It reads the state, picks the single step that is due, and hands it to the skill that teaches it. The learner never has to know which skill does what.

Read first: `../../shared/data-contract.md` and `../../shared/rules.md`. Read `## Preferences` in `profile.md`; they override defaults.

## Pick the step

Run `study status`. Note whether this is a **scheduled run** (the prompt says so) or a **chat** (the learner is here). Keep the `rev` value from `state`, and pass it as `--expect <rev>` to every `study state` call.

**Gates.** Take the first gate that applies; it is the whole run.

1. `"initialized": false`, or `assessed` is false: hand off to `assessment`.
2. `assessment_progress` is not `none`: hand off to `assessment` to continue the test.
3. `paused` is `yes`:
   - Scheduled run: end with the paused line from "Missed days" in `../../shared/rules.md`.
   - Chat: the learner is back. Run `study state paused=no unanswered_runs=0` and do **Re-entry** (below).
4. The learner's message contains answers to the open homework: hand off to the skill named in `open_homework` (for example `grammar:homework/2026-10-12-articles-2.md`) to grade it.

**Bookkeeping.** Silent work that runs before the day's step, in this order. It writes files and adds at most one line each to the message.

5. `homework_date` is 7 or more days ago: the homework has expired. Run `study state open_homework=none homework_date=none unanswered_runs=0` and add the line "I closed the homework from <date>; we start fresh." The next grammar lesson picks the topic up again.
6. `level_status` is `provisional` and `placed_on` is 14 or more days ago: run `assessment` in confirm mode.
7. `plan_week` is higher than `week_planned`: run `planner` in week mode.

**The day's step.** Take the first line that applies.

8. `open_homework` is set (and has no answers in this message):
   - Scheduled run: follow "Missed days" in `../../shared/rules.md`.
   - Chat: send the open homework again with its rules recap, and offer a fresh set instead.
9. `checkpoint_due` is true: hand off to `assessment` (checkpoint).
10. Today is not a study day (`study_day` is false):
    - Scheduled run: end with "No lesson today. Enjoy your day."
    - Chat: offer due reviews or an extra practice task, and do what the learner picks.
11. A session row with today's date and the same skill and step as today's slot already exists: offer the next slot or a review. Otherwise find today's slot in `## This week` of `plan.md` and hand off to its skill and mode.

## Re-entry

After a pause, or in a chat after a gap of 4 or more days with no scheduled runs in between. It is one step of its own:

1. Welcome the learner back in one line.
2. Review: `vocab` Review mode, capped at 8 chunks and 1 grammar topic.
3. A two-line recap of the last grammar topic.
4. End with the next-step line from `../../shared/rules.md`, naming the next step: "Send `/english-study:today` and we continue with <the next step>." Missed slots are dropped.

## Handing off

To hand off, load the named skill the way your app loads skills; if it is not loaded, read its `SKILL.md` from the folder next to this skill and follow it. Pass the mode and the slot details from `plan.md`.

## End of the step

The receiving skill logs the session and refreshes the dashboard. Before the turn ends, check that `study state` holds the next step and any open homework, and that your message ends with the next-step line from `../../shared/rules.md`.
