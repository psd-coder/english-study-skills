---
name: english-grammar
description: English grammar lessons with homework. Use when the learner wants a grammar lesson, an explanation of a grammar topic (present perfect, articles, conditionals), grammar homework, or homework checked.
license: MIT
---

# English grammar

One topic per lesson: explain, show it in real use, set homework, check it, and bring the topic back on a spaced schedule until it is automatic. A topic is never "done forever" after one good homework.

Read first: `shared/data-contract.md`, `shared/rules.md`, and the learner's L1 file if there is one (`shared/l1-russian.md`). Run `study status` and read `## Preferences` and `## Notes` in `profile.md`.

Modes:

- **Teach**: today's slot is a grammar lesson, or the learner asks for one.
- **Grade**: the learner sent answers to grammar homework (`open_homework` starts with `grammar:`).
- **Explain**: the learner asks about one point ("when do I use the past perfect?"). Answer it with steps 3 and 4 of Teach, offer a short practice set, and log a session.

## Teach

1. **Warm-up (2 to 4 minutes).** Skip it when no cards are due. In a scheduled run, put the warm-up items at the top of the homework instead (see `shared/rules.md`). `study cards --due --kind grammar --limit 1` and `study cards --due --kind vocab --limit 4`. Give 2 to 3 mixed items for the due grammar topic and one production prompt per due chunk. Grade them at once with `study card-grade` (`+` only for correct, unaided answers). Keep the warm-up short and separate from the new topic.
2. **Choose the topic** with `references/syllabus.md`, in this order: the topic named in today's slot; a topic whose last homework was below 80% or expired without answers (reteach it from a new angle); the topic behind the most frequent error category in the last two weeks of samples; the next topic in the syllabus order. Stay within one level of the learner's grammar level. A gap in an earlier topic of the same chain is the exception: teach that prerequisite first, whatever its level. In the first lesson, when no topic has been taught yet, take the review items from the `errors` of the latest assessment in `assessments.jsonl`.
3. **Explain** in this order: what it means, when we use it, how we build it. Meaning comes before form. Use a short timeline, a table or a contrast pair when it makes the meaning visible. Keep it to what the learner needs at their level.
4. **Show it in use**: 4 to 6 examples from the learner's world (their work and life from `## Notes`), a short dialogue, and one contrast pair with the form they confuse it with. Then real speech: contractions, common chunks, register, and the trap from the L1 file.
5. **Quick check**: 3 items in the chat, answered right now, to catch misunderstanding before the homework. In a scheduled run, these become the first 3 homework items.
6. **Homework**: `homework_new` new items plus `homework_review` items from earlier topics (due grammar cards first, then recent weak topics). Follow "Homework items" in `shared/rules.md`. Save it to `homework/<date>-<topic-slug>.md` with a short rules recap at the top and a `## Key` section at the end, then run `study state open_homework=grammar:homework/<file> homework_date=<today> next_step=grade --expect <rev>`.
7. Send the lesson: explanation, examples, the quick check, and the full homework in the chat. End with the next-step line from `shared/rules.md`, asking for the answers.
8. `study log session '{"skill":"grammar","step":"teach","topic":"...","minutes":...}'`, then `study dashboard`.

## Grade

1. Read the homework file and its key. Compare every answer. For free-production items, judge meaning and form, not only the target structure.
2. For each mistake: the correct form, why in one plain sentence, and the pattern. Group repeated mistakes into one explanation. Quote the best answer as praise.
3. Score: correct items out of the total. The topic is solid at 80% or more overall, with at least two thirds of the free-production items correct. Review items and warm-up items grade their own cards: `+` for each card whose items were all correct, `-` otherwise.
   - Solid and new: `study card-add --kind grammar --front "<topic>" --data '{"tag":"<tag>","level":"<level>"}'`, then `study card-grade <id>+`. The topic now returns in warm-ups after 1, 3, 7, 21 and 60 days.
   - Solid and already a card: `study card-grade <id>+`.
   - Not solid: `study card-grade <id>-` if it is a card. The next grammar slot reteaches it (step 2 of Teach).
4. Log one sample with the free-production answers and their errors (`study log sample`, with `words` counted). Log the session with the score.
5. If a mistake was really a missing word, add it with `english-vocab` quick-add (source "mistake").
6. `study state open_homework=none homework_date=none next_step=lesson unanswered_runs=0 paused=no --expect <rev>`, then `study dashboard`.
7. End the turn: the results, what to remember, and the next-step line from `shared/rules.md`. The next lesson waits for the learner's next message or the next scheduled run.
