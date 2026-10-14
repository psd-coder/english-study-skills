# Study folder and study.py

All learner data lives in one study folder. The default is `~/.english-study`; setup may move it. Every skill reaches it through `study.py`, which sits next to this file in the skill's `shared/` folder.

In the skills, `study` means: `python3 "<this skill's folder>/shared/study.py"`. If Python is missing, read and write the files directly by the same rules, and do the date math carefully by hand.

## Start of every run

Run `study status`. It returns the folder path, all settings, the state fields, due review counts, the plan week, whether a checkpoint is due, the last session and the streak. Read it before you say anything to the learner. If it reports `"initialized": false`, the learner has no study folder: hand off to `english-assessment`.

## Files

| File | Who writes it | What it holds |
|---|---|---|
| `profile.md` | `study set`, or the learner by hand | `## Settings` (one `key: value` per line), `## Preferences` (free text rules from the learner), `## Notes` |
| `state.md` | `study state` | `## Fields`: `rev`, `updated`, `next_step`, `open_homework`, `homework_date`, `unanswered_runs`, `paused`, `assessment_progress`, `week_planned` |
| `plan.md` | english-planner | roadmap, current block, `## This week` |
| `homework/<date>-<slug>.md` | the skill that sets homework | the rules recap, the items, and a `## Key` section |
| `cards.jsonl` | `study card-add`, `study card-grade` | review cards for chunks (`vocab`) and grammar topics (`grammar`) |
| `sessions.jsonl` | `study log session` | one row per finished step |
| `samples.jsonl` | `study log sample`, `study import-stream` | checked learner text with its errors, for error rates |
| `assessments.jsonl` | `study log assessment` | placement tests and checkpoints |
| `episodes.jsonl` | `study log episode` | listening and reading sources already used |
| `streams.json` | `study import-stream` | connected error streams and how far each was read |
| `progress.html` | `study dashboard` | the progress page |

Write the markdown files through `study set` and `study state` when a command exists for the change. Both commands accept only the keys listed in this file. Edit `plan.md`, homework files and the free-text sections of `profile.md` directly.

State fields:

- `next_step`: a short hint for humans (`assessment`, `plan`, `lesson`, `grade`). `english-today` decides from all fields, not from this one alone.
- `open_homework`: `none`, or `<skill>:<detail>`, for example `grammar:homework/2026-10-12-articles-2.md` or `practice:mission:<text>`.
- `homework_date`: the date the open homework was set, or `none`.
- `unanswered_runs`, `paused`: see "Missed days" in `rules.md`.
- `assessment_progress`: `none`, or the sections finished so far, for example `grammar-vocab:B1,reading:B2`.
- `week_planned`: the plan week the planner last wrote.

## Settings

`name`, `l1`, `minutes_per_day`, `days` (e.g. `mon,tue,wed,thu,fri`), `homework_new`, `homework_review`, `new_chunks_per_day`, `l1_cue_share` (`auto` or a number 0-100), `focus`, `weight_input`, `weight_output`, `weight_language`, `weight_fluency`, `level_overall`, `level_grammar`, `level_vocabulary`, `level_reading`, `level_listening`, `level_speaking`, `level_writing`, `level_status` (`none`, `provisional`, `confirmed`), `goal`, `deadline`, `plan_start`, `checkpoint_weeks`, `next_checkpoint`, `transcriber` (`handy-parakeet` or `none`), `schedule` (`none` before setup, `manual` when the learner prefers no schedule, or the app, days and time).

Homework size by daily time, used when setup writes the profile: 15 min: 8 new + 3 review. 30 min: 12 + 4. 45 min or more: 16 + 4.

## Changing settings by request

Any skill handles a request such as "make homework 16 plus 4", "no lessons on Friday" or "use fewer Russian hints". Map it to a setting, run `study set <key> <value>`, confirm the change in one line, and say it applies from the next run.

- Fewer or more first-language hints: take the current `l1_cue_share` from `status` (it is computed when the setting is `auto`), halve it for "fewer", add 15 for "more" (60 at most), and set the number. "Back to normal" sets `auto`.
- Different study days or time: also rewrite `## This week` in `plan.md` for the new days, update the `schedule` setting, and tell the learner to change the time or days in their app's scheduled task (see the planner's scheduling reference).

A rule with no setting ("use IT examples", "always repeat the rule before homework") goes as one line under `## Preferences` in `profile.md`: edit the file directly. Every skill reads Preferences at the start and follows them.

## Writing state safely

Two sessions can run at the same time (a scheduled run and a manual chat). Every state change increases `rev`. Pass the `rev` value you read in `status` to every state change: `study state next_step=grade --expect <rev>`. If the command refuses, another session moved on: run `status` again and act on the new state. After your own write, use the new `rev` it prints.

## Review cards

One Leitner schedule serves chunks and grammar topics. Boxes 1 to 5 wait 1, 3, 7, 21 and 60 days.

- A new card sits in box 0 and is due at once.
- `study card-grade 12+ 13-` grades cards. `+` means the learner produced it correctly without help, and the card moves up one box. `-` means wrong or helped: the card goes back to box 1, and a new card stays new (box 0, due tomorrow).
- A second `+` on the same day is ignored, so a card climbs only on separate days.
- After box 5 the card is mastered and stops coming back.
- Pass `--cue l1` when the prompt was in the learner's first language, `--cue context` for an English gap, `--cue free` for free use in a task.

`study cards --due --kind vocab --limit 10` lists what to review, oldest due first.

## Errors and samples

Every piece of learner English you check is logged as one sample: one written text, one spoken answer, one assessment answer, or the free-production items of one homework together:

```
study log sample '{"source":"writing","words":143,"errors":[{"category":"article","wrong":"in office","right":"in the office","rule":"...","topic":"articles"}]}'
```

`words` is the word count of the learner's own text. It is the denominator of the error rate, so count it for every sample, including clean ones (`"errors": []`). Gap-fill items are not samples; they go into the session score.

Categories: `article`, `tense`, `preposition`, `wordorder`, `agreement`, `collocation`, `phrasal`, `countability`, `spelling`, `capitalization`, `vocabulary`, `other`. `topic` is optional and names the grammar topic tag from the syllabus.

## Sessions

Log one row when a step ends:

```
study log session '{"skill":"grammar","step":"grade","topic":"Articles 2","minutes":25,"score":[14,16],"summary":"..."}'
```

Then run `study dashboard` to refresh the progress page. It prints `{"path": ...}`.
