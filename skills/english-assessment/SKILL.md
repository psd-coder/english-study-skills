---
name: english-assessment
description: English level test and study setup. Use when the learner wants to start learning English with a plan, find out their level, take a placement test, or when a 6-week checkpoint or a level confirmation is due.
license: MIT
---

# English assessment

Sets up the study folder, runs a short adaptive placement test (about 20 minutes, never more than 25), runs the 6-week checkpoint test (15 to 20 minutes), and confirms a provisional level from lesson data. It hands the result to `english-planner`.

Read first: `shared/data-contract.md` (the study folder and the `study` command) and `shared/rules.md`. If `l1` is Russian, also `shared/l1-russian.md`.

Run `study status` and pick the mode:

- `"initialized": false`: **Setup**, then **Placement**.
- Initialized, no assessment yet, or `assessment_progress` is not `none`: **Placement** (resume from the saved section).
- `checkpoint_due` is true, or the learner asks for a re-test: **Checkpoint**.
- `level_status` is `provisional` and `placed_on` (from status) is 14 or more days ago: **Confirm**.
- The learner asks "what is my level" with a recent assessment: report the latest result from `assessments.jsonl`, with its date and status.

## Setup

Follow `references/setup.md`. It ends when `study status` shows the folder with name, `l1`, time, days and focus filled in.

## Placement

1. Tell the learner the plan before the first item: "The test takes about 20 minutes: grammar and vocabulary 8, reading 4, listening 4, writing and speaking 5. You can stop after any part and continue later." Ask them to answer without a dictionary or translator, because the plan is only as good as the result.
2. Run the sections in this order, with the items and branching rules in `references/test-items.md`: grammar and vocabulary, reading, listening, production.
3. After each section, save the result: `study state assessment_progress=<section>:<level>,... --expect <rev>`. When the learner returns, continue from the next section.
4. Score with `references/scoring.md`. Every sub-skill gets a CEFR level backed by quoted evidence.
5. Save:
   - `study log assessment '{"kind":"placement","levels":{...},"overall":"B1","ielts_estimate":"5.0","toefl_estimate":"38-46","evidence":"...","focus":"..."}'`
   - `study set level_overall B1`, and the same for each `level_<skill>`; `study set level_status provisional`.
   - One sample per production answer (`study log sample`), so error rates start from day one.
   - `study state assessment_progress=none next_step=plan --expect <rev>`.
   - `study log session '{"skill":"assessment","step":"placement","minutes":<n>}'`, so the test day counts as a study day.
6. Present the result in the format from `references/scoring.md`. Say it is provisional: the first two weeks of lessons will confirm or adjust it.
7. Ask about the goal: what the learner wants to do in English (work calls, emails, travel, an exam), and by when. Save `study set goal "<goal>"` and `study set deadline <date or none>`.
8. Hand off to `english-planner` to build the program.

## Checkpoint

The same four sections, shorter (about 15 to 20 minutes): 6 to 8 grammar and vocabulary items built from the grammar topics and chunks of the last block (about 6 minutes), one short reading text one level above the reading level (about 3 minutes), one listening episode one level above the listening level (about 4 minutes), and one written and one spoken answer (about 5 minutes). Also read `study stats --weeks 6` and the session scores.

A level goes up only when the test items at the new level are clean and the production shows the same level. Write the result with `"kind":"checkpoint"`, update the `level_*` settings, set `level_status confirmed`, and hand off to `english-planner` for a re-plan; the re-plan sets the next checkpoint date. Tell the learner what moved, what did not, and the evidence for both.

## Confirm

No test. Read `samples.jsonl`, the session scores and the grammar topic results since the placement. If they fit the provisional levels, set `level_status confirmed`. If they clearly show a different level for a sub-skill (for example, homework at that level is consistently above 90% with clean free production, or consistently below 60%), change that level, log an assessment with `"kind":"confirm"`, and tell the learner in two lines what changed and why. Then return to the step that called you.
