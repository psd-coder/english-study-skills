# Listening, reading and pronunciation sources

Use real recordings by real speakers. The skills link to the material and fetch transcripts only to write questions; the learner listens and reads on the source site. Before you pick an episode, check `study episode-used <url>`, and after the learner uses it, log it: `study log episode '{"source":"elllo","url":"...","title":"...","level":"B1"}'`.

Fetch pages with `curl -sL <url>`. Some sites (BBC) block web-fetch tools but answer curl. If every fetch fails (no network, or a sandbox without network access), say so. In a test, mark listening as not assessed. In practice, give the learner the link, ask them to listen and write a 3 to 5 sentence summary, and check that summary as a writing sample.

## Listening by level

| Source | Levels | What you get | Notes |
|---|---|---|---|
| ELLLO, `https://elllo.org` | A1-C1, tagged by CEFR | short real conversations, audio or video, transcript on the page | main source for A1-B2; episode pages like `elllo.org/english/1451/1451-AimeeTodd-Favorites.htm` |
| BBC Learning English, 6 Minute English | B1-C1 | 6-minute episode, transcript on the page, PDF and MP3 | main source for B1-C1; episodes at `bbc.co.uk/learningenglish/english/features/6-minute-english_<YYYY>/ep-<YYMMDD>`; fetch with curl |
| VOA Learning English, `https://learningenglish.voanews.com` | Beginning, Intermediate, Advanced | slow, clear news with full text | public domain; extra source, check that new episodes still appear |
| TED, `ted.com/talks/<slug>/transcript` | C1 and above | talks with full transcripts | natural fast speech; no level tags; licence CC BY-NC-ND, so link only |
| Plain English, `https://plainenglish.com` | B1-B2 | current-events podcast with transcripts | extra source |

Pick by the learner's listening level: one level above for a stretch task, the same level for fluency work.

To find recent BBC episodes, fetch `https://www.bbc.co.uk/learningenglish/english/features/6-minute-english` and collect the links that contain `/ep-`. The six digits after `ep-` are the date (YYMMDD), so sort them and start from the newest. For ELLLO, the level pages on `https://elllo.org` list episodes by CEFR level.

## Pronunciation of a word or phrase

- Cambridge Dictionary: `https://dictionary.cambridge.org/dictionary/english/<word>`. The page has UK and US recordings by real speakers. To give a direct audio link, fetch the page with curl and take the `.mp3` paths under `/media/english/uk_pron/` and `/media/english/us_pron/`; the file names do not follow the word, so read them from the page.
- YouGlish: `https://youglish.com/pronounce/<word or phrase>/english/us` (or `/uk`, `/aus`). Real people saying it in videos. The page blocks automated fetching, so give it as a link only.
- Forvo: `https://forvo.com/word/<word>/#en`. Many native speakers. Link only.

## Shadowing material

Shadowing means the learner plays a short phrase, pauses, and repeats it with the same rhythm and stress. Take the lines from the listening episode the learner just finished: you have its transcript, and the learner already knows the content. Choose 3 to 5 lines of 6 to 15 words with the week's target sounds or chunks, and give the timestamp or the paragraph where each line is.

For single sentences, Tatoeba (`https://tatoeba.org`) has sentences with recordings by people; each recording has its own licence, so link to the sentence page.
