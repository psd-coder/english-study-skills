# Setup

About 3 minutes. Ask the questions in one or two messages, not one by one.

1. Say what happens: "First a few questions to set things up (3 minutes), then a test of about 20 minutes. After that I build your study plan."
2. Ask:
   - Their name, and their first language.
   - How many minutes a day they can study (15, 30, 45 or 60) and on which days.
   - What they want to focus on more, if anything: speaking, listening, reading, writing, grammar, vocabulary. "No preference" is a good answer.
   - Their work and daily life in one or two lines, so examples come from their world.
   - Where to keep the study files. Offer the default `~/.english-study` and accept any folder.
3. Create the folder: `study init --name "<name>" --l1 "<language>"`, adding `--dir <path>` only if they chose another folder. A custom folder is also saved in `~/.config/english-study/location`, so every skill finds it later.
4. Save the answers with `study set`:
   - `minutes_per_day`, `days`.
   - `homework_new` and `homework_review` by time: 15 min: 8 and 3. 30 min: 12 and 4. 45 min or more: 16 and 4.
   - `new_chunks_per_day`: 15 min: 4. 30 min: 6. 45 min or more: 8.
   - `focus`: their focus words, or `none`.
   - Write the work and life lines under `## Notes` in `profile.md`.
5. Speaking setup. Speaking practice needs Handy, a free dictation app that writes down what the learner says. Ask if they want speaking practice. If yes, give these steps:
   - Download Handy from `https://handy.computer` and open it.
   - In Settings, choose the model **Parakeet V3**.
   - In Advanced, turn **Filler Word Removal** off, and keep **Post-processing** off. Both change what the learner said, and we need the real words to give real feedback.
   - Test: hold the Handy shortcut, say one sentence, and check it appears in the chat.
   If they say no or it does not work, run `study set transcriber none`; speaking is then trained through real-life tasks only, and the speaking test answer is typed.
6. Tell them they can change any of this later by asking, for example "make lessons 45 minutes" or "no lessons on Friday".
