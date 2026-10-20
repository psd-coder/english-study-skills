---
name: practice
description: English listening, reading, writing and speaking practice. Use when the learner wants to practise listening to real English, read a text, write something and get it corrected, practise speaking, or do a fluency or shadowing exercise.
license: MIT
---

# English practice

The input, output and fluency strands of the plan, with real material and focused feedback. Each mode has the same shape: a task with a clear purpose, the learner's work, feedback, and a log entry.

Read first: `../../shared/data-contract.md` and `../../shared/rules.md`. Run `study status` and read `## Preferences` and `## Notes` in `profile.md`.

Pick the mode from today's slot in `plan.md` or from the learner's request, then follow its reference file:

| Mode | Reference | Strand |
|---|---|---|
| listening | `references/listening.md` | input |
| reading | `references/reading.md` | input |
| writing | `references/writing.md` | output |
| speaking | `references/speaking.md` | output |
| fluency (timed retell, 4-3-2 speaking, speed reading, shadowing) | `references/fluency.md` | fluency |

## In every mode

1. **Warm-up**: run `vocab` review for up to 5 due cards, unless the session is under 15 minutes.
2. Say the purpose of the task in one line ("Today: following a real conversation at natural speed, and two useful chunks from it").
3. Do the mode.
4. Pull 2 to 4 useful chunks out of the material or the learner's errors and add them with `vocab` quick-add (source listening, reading or mistake). Tell the learner which ones you added.
5. Log the work:
   - Every checked piece of the learner's own English as a sample (`study log sample`, with `words`).
   - Every listening or reading source with `study log episode`.
   - The session with its score: `study log session '{"skill":"practice","step":"<mode>",...}'`.
6. If the mode left a task open (a rewrite, a speaking retry), record it: `study state open_homework=practice:<mode>:<short note> homework_date=<today> next_step=grade --expect <rev>`. Grading it later is one step; close it with `open_homework=none homework_date=none unanswered_runs=0 paused=no`.
7. Run `study dashboard`, and end with the next-step line from `../../shared/rules.md`.
