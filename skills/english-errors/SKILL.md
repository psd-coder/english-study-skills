---
name: english-errors
description: Connect an English error stream to the study plan. Use when the learner wants to import mistakes from another tool (a writing checker, an English coach hook, a log of corrected messages), connect such a log, or refresh imported errors. For advanced users.
license: MIT
---

# English error streams

A stream is a file that another tool keeps filling with corrected English: the learner's real messages and the mistakes found in them. Imported entries become samples, so they count in the error rate, guide the choice of grammar topics, and show whether real writing improves, not only homework.

Read first: `shared/data-contract.md`. Run `study status`.

## Connect a stream

1. Ask for the file path and look at the last 40 lines to find the format:
   - **coach**: blocks that start with `English check`, usually with each line prefixed by `│` and sometimes closed by a `╰─` border line, with `Yours:`, `Fixed:` and numbered mistakes like `1. [article] wrong -> right`. This is the format of the english-coach hook log (`~/.claude/english-coach.log`).
   - **jsonl**: one JSON object per line, in the format below.
   - Anything else: show the learner the jsonl format and ask them to make their tool write it, or write a small converter for them.
2. Connect it with a first import: `study import-stream <path> --format <coach|jsonl> --name <short-name>`. The first import reads the whole file. The stream is now saved in `streams.json`, and every later refresh reads only new lines.
3. Tell the learner how many entries came in and what the top error categories are (`study stats --weeks 2`).

## Refresh

`study import-stream` with no path refreshes every connected stream. A missing file is reported and skipped; tell the learner in one line. The planner refreshes streams every week and the progress report before it runs.

## The jsonl format

```
{"date": "2026-10-14", "words": 42, "text": "optional original text", "errors": [{"category": "article", "wrong": "in office", "right": "in the office", "rule": "optional"}]}
```

`date` is optional (the import date is used). `words` is the word count of the learner's text; entries without it count as error examples but not in the error rate. Categories are listed in `shared/data-contract.md`; unknown ones become `other`.

## Limits to tell the learner

The coach format has no dates, so entries get the date of the import; refresh often (the planner does it weekly) to keep weeks accurate. Clean messages in the coach log carry no text, so only messages with errors count words, and the coach error rate is higher than the true rate. For this reason streams have their own line in `study stats` (`stream_rate_per_100`) and their own chart on the dashboard: compare a stream with itself over time, not with the lesson samples.
