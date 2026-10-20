---
name: english-progress
description: English study progress report and dashboard. Use when the learner asks how they are doing, wants to see their progress, stats, streak or level, or asks what improved.
license: MIT
---

# English progress

Shows the learner an honest picture: what improved, what did not, and what that means for the next weeks.

Read first: `../../shared/data-contract.md` and `../../shared/rules.md`.

1. Run `study import-stream` (refreshes connected error streams, if any), then `study status` and `study stats --weeks 8`.
2. Run `study dashboard`. In a chat, open the page: `open <path>` on macOS, `xdg-open <path>` on Linux, `start <path>` on Windows. In a scheduled run, or if opening fails, give the path instead.
3. Write a short report (8 to 12 lines):
   - Consistency: sessions and hours in the last 4 weeks, and the streak.
   - Accuracy: errors per 100 words now against 4 weeks ago, overall and for the two most frequent categories. This is the main measure of real progress, because it comes from the learner's free writing and speaking, not from exercises.
   - Knowledge: chunks and grammar topics by stage (learning, reviewing, mastered), and the topics that failed a re-check.
   - Level: the current levels with their status (provisional or confirmed) and the date of the next checkpoint. Homework scores show progress inside a level; only a checkpoint changes the level.
   - One clear next focus, in plain words.
4. When a number cannot be computed yet (fewer than two weeks of samples), say so instead of guessing.

No session log: this is not a study step.
