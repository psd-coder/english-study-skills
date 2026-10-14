# Speaking

The learner speaks; Handy turns the speech into text; you give feedback on what they really said. If `transcriber` is `none`, use real-world missions (below) and say that speaking feedback needs Handy (setup in the `english-assessment` skill, `references/setup.md`).

## What the transcript can and cannot show

Handy with Parakeet keeps most grammar and word errors, so feedback on accuracy and range is reliable. It may drop filler sounds (um, er) and it joins repeated words, so hesitation is partly hidden. It cannot show pronunciation. Tell the learner this the first time, in one or two lines, and never give a pronunciation score.

## First speaking task after a late Handy setup

If `level_speaking` is `not assessed` and Handy now works, the first speaking task also measures the level. Use a production prompt from `english-assessment` (`references/test-items.md`, section 4) at the learner's overall level, score it with that skill's `references/scoring.md`, then `study set level_speaking <level>` and `study log assessment '{"kind":"speaking","levels":{"speaking":"<level>"}}'`.

## A speaking task

1. **Prompt**: a real situation from the learner's life or goal: explain a problem to a client, give an update in a stand-up meeting, tell a story from the week, give an opinion on the listening episode. Give 30 seconds to think, with 2 or 3 points to cover, and a target length: 60 seconds for A2-B1, 90 to 120 seconds for B2 and up.
2. **Speak**: "Hold the Handy shortcut, speak, and send the text without changing it. Note how many seconds you spoke." No writing first; the point is speaking in real time.
3. **Feedback**:
   - The corrected version of what they said, keeping their meaning.
   - The top 2 or 3 patterns, as in writing feedback.
   - Range: one or two chunks that would make it sound more natural ("Long story short...", "The thing is...").
   - Fluency, as a rough number: words divided by the seconds they reported, times 60. Around 100 words per minute is a comfortable speaking pace for a learner; name the trend, not the exact value. Call it rough, because of what the transcript hides.
4. **Second try**: the same prompt again, using the corrections and one new chunk. The second version is almost always better; point out exactly what improved.
5. **Log** both answers as samples (`"source":"speaking"`).

## Shadowing

From the latest listening episode, 3 to 5 lines (see `shared/sources.md`). The learner plays each line, pauses, repeats it out loud matching the rhythm and stress, three times, and then says it once into Handy. Compare the words with the transcript and point out dropped small words (articles, prepositions, endings). For words they are unsure how to say, give the Cambridge and YouGlish links.

## Real-world missions

A small task to do in real life before the next speaking slot: "In Thursday's call, use 'the thing is' once and ask one follow-up question", "Leave a 30-second voice message in English to a colleague". Write the mission into `open_homework` as `practice:mission:<text>`. Next time, ask how it went, what was hard and which words were missing, and add those words with `english-vocab` quick-add.
