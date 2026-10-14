# Test items and branching

The test looks for the learner's ceiling: the level where errors become regular. It does not give every item. All items below are original; write fresh items in the same style when you need more, and never copy real exam papers.

## Rules for every section

- Send 2 to 4 items per message. React in a few words ("good", "noted") and keep answers to yourself until the end.
- Start at B1. Two clean items at a level: move up one level. Two broken items: move down one level. The level where the learner handles most items but breaks down one level higher is their level for that section.
- Keep to the time budget. When the level is clear, stop that section.
- In checkpoint mode, replace the bank items with items built from the topics and chunks of the last block.

## 1. Grammar and vocabulary (about 8 minutes, 8 to 12 items)

Alternate grammar and vocabulary items, and track two ceilings: one for grammar and one for vocabulary. Each gets its own level. Use gap-fill, error correction and transformation.

**A1**: "She ___ (be) a teacher and she ___ (live) in Madrid." / Correct: "He don't likes coffee." / Opposite of *cheap*? / "a ___ of milk: bottle, piece, slice".

**A2**: "Yesterday we ___ (go) to the beach and ___ (swim) all afternoon." / Correct: "She is more taller than her brother." / "I'll see you ___ Monday, ___ the morning, ___ 6 o'clock." / Odd one out: furious, annoyed, delighted, irritated.

**B1**: "I ___ (know) her since 2018." / "It started raining two hours ago." -> "It ___ for two hours." / Correct: "If it will rain tomorrow, we stay home." / "Make or do a decision?" / Use *give up* in a sentence.

**B2**: "By the time we arrived, the film ___ (already, start)." / "People say he is very rich." -> "He ___ to be very rich." / "If I ___ (study) harder last year, I ___ (pass)." / Correct: "I look forward to meet you." / Make formal: "I wanna ask about the job." / *heavy rain, strong rain or big rain*?

**C1**: "I had never seen anything like it." -> "Never ___." / Rewrite to stress the cause: "We lost because of poor planning." / "If I ___ (be) more careful, I ___ (not be) in this mess now." / Difference between *consequence* and *repercussion*? / Noun, adjective and adverb of *strength*? / "a ___ distinction, a ___ argument".

## 2. Reading (about 4 minutes)

One passage at the level from section 1, three questions: one fact, one inference, one word in context. Give a second passage one level up only if the first was clean and the ceiling is still unclear.

**A2** (70 words): Mara works in a small bakery near the station. She starts at five in the morning, when the streets are still empty and quiet. She likes this time best because the shop smells of fresh bread and nobody is in a hurry yet. By eight o'clock the bakery is full of people buying their breakfast, and Mara is always busy until lunch.
Questions: What time does Mara start work? Why does she like the early morning? What does "in a hurry" mean?

**B1** (110 words): When the town announced it would close the old library, almost no one expected the reaction that followed. Within a week, hundreds of residents had signed a petition, and a group of teenagers organized a weekend of readings on the library steps. The council had assumed the building was barely used; the protests suggested otherwise. What people seemed to value was not only the books, but a free, warm place to sit that belonged to everyone. In the end the council postponed its decision and promised a review.
Questions: What did the council plan to do? Why were they surprised? What does "postponed" mean here?

**B2** (140 words): The promise of remote work was freedom: no commute, no fixed desk, no manager hovering nearby. For some, that promise has held. For others, the boundary between work and home has quietly dissolved, so that the laptop on the kitchen table is never truly closed. Productivity studies tell a mixed story: output often holds steady or rises, while the sense of being "always on" erodes the very wellbeing remote work was supposed to protect. The lesson emerging is not that remote work is good or bad, but that it shifts responsibility for boundaries from the office to the individual, and not everyone is equally equipped to draw them.
Questions: What happened to the work-home boundary for some people? What is the main point of the last sentence? What does "erodes" mean here?

**C1** (170 words): It is tempting to treat nostalgia as a harmless indulgence, a soft-focus longing for a past that never quite existed as we remember it. Yet the emotion is more double-edged than it appears. Psychologists have found that nostalgia can buffer against loneliness and lend a sense of continuity to a life in flux; recalling a warm shared meal can make the present feel less precarious. The same backward gaze, however, can curdle into a conviction that everything good is already behind us, a stance that quietly forecloses the future. What distinguishes the restorative kind from the corrosive kind is not the intensity of the feeling but its direction: whether the remembered past is used as a resource for living now, or as a verdict against the present.
Questions: What good effects of nostalgia does the writer mention? What danger does the writer see? In your own words, what separates restorative from corrosive nostalgia?

## 3. Listening (about 4 minutes)

Real recordings only (see `shared/sources.md`). Pick an episode at the current estimate: ELLLO for A1 to B2, BBC 6 Minute English for B1 to C1.

1. Fetch the page with curl and read the transcript. Choose a 1 to 2 minute stretch. Transcripts have no timestamps, so count about 130 words per minute: for BBC, the first 250 words of the transcript are about the first two minutes.
2. Give the learner the link and say exactly what to listen to ("the first 2 minutes", "the whole clip"). Ask them to keep the transcript closed and to count how many times they play it.
3. Ask three questions from that stretch: the main idea, one detail, and one thing the speaker implies or feels.
4. Log the episode with `study log episode`.

Scoring: the level is the highest level where the learner got the main idea and the detail. If they needed 3 or more plays, use the level below. If no episode can be fetched, mark listening as "not assessed" and plan a listening task in week 1 to measure it.

## 4. Production (about 5 minutes)

One written answer and one spoken answer, at the tier that matches the estimate (one tier up if the estimate is B2 or higher).

- Tier 1 (A2): "Tell me about a normal day for you, from morning to evening."
- Tier 2 (B1): "Tell me about the last trip you took. What happened?"
- Tier 3 (B2): "Some people think working from home is better than working in an office. What do you think, and why?"
- Tier 4 (C1): "If you could change one thing about how English is taught, what would it be, and what difference would it make?"

Written: ask for 60 to 120 words, typed without a translator.

Spoken: the learner holds the Handy shortcut and speaks for about 60 to 90 seconds, then sends the text without editing it. Say: "Do not fix the text; I need to see what you really said." If `transcriber` is `none`, take a second typed answer and set `level_speaking` to `not assessed`. The first speaking task after Handy is set up measures it.

Look at how the learner builds sentences: tense control, articles, linking words (*because, so* or *whereas, although*), sentence length and clauses, word precision, and errors that repeat. A repeated error is the strongest level signal.
