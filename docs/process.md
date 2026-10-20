# How the study process works

This document describes the study process itself. It does not depend on one app: any AI agent that can read and write files and run a command can follow it. Claude Desktop, Claude Code and Codex all work.

## The cycle

The learner starts with one conversation that takes about 25 minutes. Setup asks a few questions and creates the study folder (3 minutes). Then a placement test of about 20 minutes covers grammar and vocabulary, reading, listening to a real recording, one written answer and one spoken answer. The result is a CEFR level for each skill, marked as provisional. After that, the agent asks about the goal and the deadline and builds a program.

After that, every study day has one session of 15 to 45 minutes, depending on the learner's settings. A session starts with a short review of items that are due, then does the one activity that the week's plan sets for that day. Homework is checked in a separate step, when the learner sends the answers.

Every week, the plan is rebuilt from the last week's results. Every six weeks, a 15 to 20 minute checkpoint test measures the level again, and the program is planned again from the new result.

## What a week contains

The plan splits study time across four strands, a model from the language researcher Paul Nation. Each strand starts at 25% of the time.

- Input: listening and reading real material for meaning.
- Output: writing and speaking to say something real, with feedback.
- Language: grammar lessons and vocabulary chunks studied directly.
- Fluency: easy, known material used faster (timed retelling, 4-3-2 speaking, speed reading, shadowing).

At setup the learner can name a focus, and the starting weights move toward it. Each week the planner moves up to 10 points toward the strand with the worst trend. More errors in speaking gives more output time. Low listening scores give more input time.

## Why it is built this way

Each method has research behind it, and each one also fixes a problem from an earlier version of this setup.

Words and grammar topics come back after 1, 3, 7, 21 and 60 days, and the learner has to produce them, not only recognise them. This is spaced retrieval practice. A grammar topic stays in the review cycle after a good homework. The earlier version marked 45 topics as "learned" in seven weeks, and the learner still forgot conditionals.

Review cards ask the learner to say or write the chunk. Some cards give the prompt in the learner's first language. Their share falls as the level rises, from 50% at A1-A2 to 30% at B1, 15% at B2 and 5% or less at C1.

Writing and speaking feedback gives the full corrected text, then explains only the two or three patterns that repeat, and asks for a short rewrite. Research on written corrective feedback supports this focused form over correcting everything at once.

Listening uses real recordings with transcripts. ELLLO covers A1-B2 and BBC 6 Minute English covers B1-C1. Pronunciation links go to Cambridge Dictionary recordings and YouGlish. Synthetic speech is never used, because it can teach wrong pronunciation.

The level changes only through a test, and IELTS and TOEFL numbers are always marked as estimates. Good homework scores count as progress inside a level. The main progress measure is errors per 100 words in the learner's own writing and speaking.

## Rules for every session

A run does one step and ends. After homework is graded, the turn ends, and the next lesson waits for the learner or for the next scheduled run.

The chat holds the whole lesson, with the rules, the examples and every exercise. The files are the record. Homework uses new sentences in a shuffled order, and at least a quarter of it is free production.

After two scheduled runs with no answer, the next run sends one message that says the study is paused. The study stays paused until the learner comes back. Missed lessons are dropped, so the learner never faces a backlog. The learner can change any setting by asking. Personal rules go into the profile, and every skill follows them.

## Where the data lives

All data stays in one local folder, `~/.english-study` by default. `profile.md` holds the settings and personal rules, and the learner can edit it. `plan.md` holds the roadmap and the week's plan, and `state.md` the next step and any open homework. Each homework is a file in `homework/` with its answer key. The `.jsonl` logs keep review cards, sessions, checked text with errors, tests and the episodes already used. `progress.html` is the progress page, opened by asking "show my progress".

A small Python script, `study.py`, does the date math, review scheduling and statistics. It uses only the standard library. If Python is missing, the agent edits the files by the same rules.

## Speaking

The learner speaks into Handy, a free dictation app, with the Parakeet V3 model. Filler-word removal and post-processing must be off. The transcript keeps most grammar and word errors, so feedback on accuracy is reliable. Handy can drop filler sounds and it joins repeated words, so fluency is measured only roughly (words per minute from the time the learner reports). The transcript shows nothing about pronunciation, and the skills never give a pronunciation score. Pronunciation help comes from the dictionary and YouGlish links and from shadowing lines of real recordings.

## Running it on a schedule

Scheduled runs work in Claude Desktop (Code tab), Cowork and the Codex app while the app is open, and through cron with `claude -p` or `codex exec`. Without a schedule, the learner calls `english-today` by name in any chat (`/english-today` in Claude Code), and the agent works out what is due from the study folder.
