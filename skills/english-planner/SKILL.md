---
name: english-planner
description: English study program and weekly plan. Use after an English assessment or checkpoint, at the start of each study week, when the learner wants to change goal, focus or schedule, or wants lessons to run automatically on a schedule.
license: MIT
---

# English planner

Turns the assessment into a program, writes each week's plan, and sets up the daily schedule. The plan decides what each session trains; the other skills follow it.

Read first: `shared/data-contract.md` and `shared/rules.md`. Run `study status`.

Modes:

- **Program**: after a placement or checkpoint, or when the goal changes.
- **Week**: the first run of a new plan week (`plan_week` from status is higher than the state field `week_planned`). `english-today` calls this mode.
- **Schedule**: the learner wants automatic lessons, or Program has just finished.

## Program

Follow `references/planning.md`:

1. Feasibility check: hours needed against hours available, with an honest verdict, and a re-scoped goal when the verdict is "not realistic". Save the goal you plan for: `study set goal "<goal>"`.
2. Strand weights: start from 25% each for input, output, language and fluency. Move up to 10 points toward the learner's `focus` and up to 10 points toward the weakest sub-skill. Save them with `study set weight_<strand> <n>`; the four always sum to 100.
3. Roadmap: 6-week blocks, each ending with a checkpoint. Name what the learner will be able to do at the end of each block, in their goal's terms.
4. Write `plan.md` (format in `references/planning.md`). Every program, the first and every re-plan, starts its own week count: set `plan_start` to the Monday of the current week, `next_checkpoint` to `plan_start` plus `checkpoint_weeks` weeks, run `study state week_planned=0 next_step=lesson --expect <rev>`, and run **Week** for week 1. When the program starts on a Thursday or later, week 1 holds only the remaining days.
5. Run **Schedule** if the `schedule` setting is `none`. If the learner prefers to start lessons by hand, set `schedule manual` and do not offer it again.
6. Show the learner the roadmap, week 1 and the schedule steps in one message. End with the first step: "Your first lesson is ready. Say 'start' or wait for the schedule."

## Week

Silent bookkeeping that runs before the day's step; the learner sees one or two lines about the new week.

1. Run `study import-stream` (it refreshes connected error streams and does nothing when there are none). Then read `study stats --weeks 2`, the last week's sessions and their scores, and which slots were skipped.
2. Rebalance: move at most 10 points between strands, toward the strand with the worst trend. Error rate up in writing or speaking: more output. Low listening or reading scores: more input. Homework below 70% two weeks running: more language. Long pauses or very short answers in speaking: more fluency. Save the new weights.
3. Choose the week's themes: the grammar focus (from the most frequent error categories in recent samples), a chunk theme that serves the goal, and the listening level.
4. Lay out the slots with `references/planning.md` (slot allocation) and write `## This week` in `plan.md`.
5. `study state week_planned=<plan_week> --expect <rev>`.

## Schedule

Follow `references/scheduling.md` for the learner's app. Ask before you create anything. Always print the ready-to-paste prompt and the click-by-click steps, even when you also create the task with a tool. Save `study set schedule "<app> <days> <time>"` when it is done.
