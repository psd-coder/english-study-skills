---
name: english-vocab
description: English vocabulary with spaced review. Use when the learner wants to add a word or phrase to learn, review their words, learn new words or collocations on a topic, or asks how a word is used or pronounced.
license: MIT
---

# English vocabulary

Builds a store of chunks (words with the words they live with: "make a decision", "reckon that...", "come up with an idea") and brings each back on a spaced schedule until the learner uses it without help.

Read first: `../../shared/data-contract.md` and `../../shared/rules.md`. If `l1` is Russian, also `../../shared/l1-russian.md` (false friends). Run `study status`.

Modes:

- **Quick-add**: the learner gives a word or phrase ("add 'nudge'", a list of words). Also used by other skills for words the learner was missing.
- **Session**: today's slot is a chunks session, or the learner wants new words on a topic.
- **Review**: due reviews only, for warm-ups, re-entry and days off. It covers due grammar topics too.
- **Grade**: the learner sent answers to vocab homework (`open_homework` starts with `vocab:`). Grade each answer as in Review step 3, correct the wrong ones, then `study state open_homework=none homework_date=none unanswered_runs=0 paused=no --expect <rev>`.

## The card

Every chunk is one card: `study card-add --kind vocab --front "<chunk>" --data '<json>'`. Data fields:

- `meaning`: a plain-English meaning at the learner's level.
- `l1`: the translation into the learner's first language.
- `example`: one natural sentence from the learner's world, and `example_l1`, its translation.
- `collocations`: 2 to 4 common partners ("strongly recommend", "recommend doing").
- `forms`: the word family (decide, decision, decisive, decisively).
- `register`: neutral, informal, formal or slang.
- `trap`: a false friend or a common misuse, if there is one.
- `source`: request, session, mistake, listening, reading or assessment.
- `pron`: the Cambridge Dictionary URL (`../../shared/sources.md`).

The front is the chunk the learner should produce, not a lone word, whenever the word has a typical partner.

## Quick-add

For each item: check `study cards --find <word>` for a card with the same core word, fill the card, add it, and reply in a few lines per chunk: meaning, translation, one example, the main collocation, and the pronunciation links (Cambridge, YouGlish). If `study card-add` says the chunk exists, say so and show its current stage instead. No practice and no session log unless the learner asks for more.

## Session

1. **Review first**: run **Review** for the due cards.
2. **Choose new chunks**: up to `new_chunks_per_day` (fewer if many reviews were due). Take them from the week's chunk theme in `plan.md`, the learner's recent mistakes, and words from recent listening and reading. Choose for frequency and use in the learner's goal.
3. **Introduce each chunk in context**: a 2 to 6 line dialogue from the learner's world where the chunk appears, then the meaning, 2 to 3 more examples in different situations, a near-synonym contrast when useful ("reckon" vs "think"), the word family, the register, and the trap. Use the learner's first language only for a one-line gloss when the meaning stays unclear.
4. **Production practice**: for each chunk, one task where the learner must produce it: answer a question with it, finish a sentence, a short role-play line, or use two new chunks in one sentence. Correct each answer. In a scheduled run, send these tasks as homework: save them to `homework/<date>-chunks.md` and run `study state open_homework=vocab:homework/<file> homework_date=<today> --expect <rev>`.
5. **Save**: add every new chunk as a card. A chunk the learner already produced correctly here gets `study card-grade <id>+ --cue free`.
6. Log the session and run `study dashboard`. End with what to look out for ("Try to use 'reckon' in a real message this week."), then the next-step line from `../../shared/rules.md`.

## Review

1. `study cards --due --kind vocab --limit <n>`, where n is about 10 for 15 minutes and 15 for 30 minutes or more, and `study cards --due --kind grammar --limit 2`. A due grammar topic gets 2 to 3 short mixed items (gap-fill, correction, one free sentence), graded as one card: `+` only when all are correct.
2. Ask for production, never recognition. For each card pick the cue type. The share of first-language cues is `l1_cue_share` from status; the rest are English context gaps.
   - Context cue: an English sentence with a gap and a hint of meaning: "We need to ___ a decision by Friday (choose)."
   - First-language cue: a sentence in the learner's language to say in English (for a Russian speaker: «Нам нужно принять решение до пятницы»).
   Use new sentences each time, not the card's example.
3. Grade: `+` only for the right chunk, produced without help (small spelling slips are fine). Anything else is `-`. Run `study card-grade 12+ 15- 18+ --cue context` (one call per cue type).
4. For each `-`, show the right answer with its example and one more quick try. The card stays at box 1.
5. Outside a warm-up, log a session (`"skill":"vocab","step":"review"`) and run `study dashboard`.
