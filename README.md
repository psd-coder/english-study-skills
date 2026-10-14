# English study skills

Eight agent skills that run a personal English program: a placement test, a weekly plan, daily lessons with homework, spaced review, real listening material, writing and speaking feedback, and a progress page. They follow the open Agent Skills format, so they work in Claude Desktop, Claude Code, Codex and other agents that can read files and run commands. All learner data stays in a local folder.

The method and the reasons behind it are in [docs/process.md](docs/process.md).

## Install

With the GitHub CLI (2.9x or newer):

```sh
gh skill install psdcoder/english-study-skills --all --scope user --agent claude-code
```

Use `--agent codex` for Codex. Run `gh skill install --help` to see the other agents.

With the `skills` CLI:

```sh
npx skills add psdcoder/english-study-skills
```

With curl, into `~/.claude/skills` (use `codex`, `agents` or a folder path instead of `claude`):

```sh
curl -fsSL https://raw.githubusercontent.com/psdcoder/english-study-skills/main/scripts/install.sh | sh -s -- claude
```

For Claude Desktop, download `english-study-skills.zip` from the latest release, unzip it, and upload each `english-*.zip` in Settings, Capabilities, Skills.

The skills need Python 3.8 or newer for `study.py`. macOS and most Linux systems already have it.

## Start

Open a chat in your agent and say "I want to study English with a plan". Setup takes 3 minutes and the placement test about 20. Then the agent builds your program and offers to set up a daily schedule.

After that, say "next lesson" whenever you want to study, or let the schedule start the lessons. Other useful phrases:

- "add 'reckon' to my words"
- "check my homework: ..."
- "show my progress"
- "make homework 16 plus 4" or "no lessons on Friday"
- "explain the present perfect"

## Skills

| Skill | What it does |
|---|---|
| `english-assessment` | setup, placement test, 6-week checkpoint, level confirmation |
| `english-planner` | program, weekly plan, schedule setup |
| `english-today` | the daily entry point: picks the step that is due |
| `english-grammar` | grammar lessons, homework, grading |
| `english-vocab` | words and chunks with spaced review |
| `english-practice` | listening, reading, writing, speaking, fluency |
| `english-progress` | progress report and dashboard |
| `english-errors` | imports errors from other tools (advanced) |

## Speaking practice

Speaking feedback needs [Handy](https://handy.computer), a free dictation app. In its settings, choose the Parakeet V3 model, turn Filler Word Removal off and keep Post-processing off. Without Handy, speaking is trained through real-life tasks.

## Schedules

| App | Works | Note |
|---|---|---|
| Claude Desktop, Code tab | yes | runs locally while the app is open |
| Claude Cowork | yes | runs in the cloud; reaches the study folder only while the app is open |
| Codex app | yes | runs locally while the app is open |
| Claude Code, Codex CLI | with cron | see `skills/english-planner/references/scheduling.md` |
| Claude Code `/schedule` | no | runs in the cloud without your files |

## Development

`shared/` is the single source for `study.py` and the shared reference files. Each skill installs on its own, so each one carries a copy in its `shared/` folder. After you change anything in `shared/`, run:

```sh
python3 -m unittest discover -s shared
scripts/sync-shared.sh
```

`gh skill publish --dry-run` checks the skills against the Agent Skills specification. To release, run `gh skill publish --tag <version>`, then `scripts/package.sh` and `gh release upload <version> dist/*.zip`, so the Claude Desktop zips are on the release page.

Still to verify: whether a scheduled task that an agent creates by writing a file in `~/.claude/scheduled-tasks/` shows up in Claude Desktop. Until then, the planner always prints the setup steps.

## License

MIT
