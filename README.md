# English study skills

A plugin with eight agent skills that run a personal English program: a placement test, a weekly plan, daily lessons with homework, spaced review, real listening material, writing and speaking feedback, and a progress page. It works in Claude Code, Claude Desktop and Codex. All learner data stays in a local folder.

The method and the reasons behind it are in [docs/process.md](docs/process.md).

## Install

The skills install together as one plugin, `english-study`. They share one `study.py` helper and one set of reference files.

In Claude Code:

```sh
claude plugin marketplace add psd-coder/english-study-skills
claude plugin install english-study@english-study-skills
```

In the Code tab of Claude Desktop, open **+**, then **Add plugins**, add the marketplace `psd-coder/english-study-skills` and install `english-study`.

In Codex:

```sh
codex plugin marketplace add psd-coder/english-study-skills
codex plugin add english-study@english-study-skills
```

The skills need Python 3.8 or newer for `study.py`. macOS and most Linux systems already have it.

## Start

Every skill is called by its full name, with the plugin name in front. In Claude Code and the Code tab of Claude Desktop, a call starts with `/`. In Codex, it starts with `$`.

To begin, send `/english-study:assessment` in Claude Code or `$english-study:assessment` in Codex. Setup takes 3 minutes and the placement test about 20. Then the agent builds your program and offers to set up a daily schedule.

After that, start each lesson with `/english-study:today`, or let the schedule start the lessons. Send your homework answers after the same call, in the same chat or a new one. The skill reads your study folder, so a new chat knows where you stopped. Other useful phrases:

- "add 'reckon' to my words"
- "show my progress"
- "make homework 16 plus 4" or "no lessons on Friday"
- "explain the present perfect"

## Skills

| Skill | What it does |
|---|---|
| `assessment` | setup, placement test, 6-week checkpoint, level confirmation |
| `planner` | program, weekly plan, schedule setup |
| `today` | the daily entry point: picks the step that is due |
| `grammar` | grammar lessons, homework, grading |
| `vocab` | words and chunks with spaced review |
| `practice` | listening, reading, writing, speaking, fluency |
| `progress` | progress report and dashboard |
| `errors` | imports errors from other tools (advanced) |

## Speaking practice

Speaking feedback needs [Handy](https://handy.computer), a free dictation app. In its settings, choose the Parakeet V3 model, turn Filler Word Removal off and keep Post-processing off. Without Handy, speaking is trained through real-life tasks.

## Schedules

| App | Works | Note |
|---|---|---|
| Claude Desktop, Code tab | yes | runs locally while the app is open |
| Claude Cowork | yes | runs in the cloud; reaches the study folder only while the app is open |
| Codex app | yes | runs locally while the app is open |
| Claude Code, Codex CLI | with cron | see `skills/planner/references/scheduling.md` |
| Claude Code `/schedule` | no | runs in the cloud without your files |

## Development

The repository root is the plugin. `.claude-plugin/plugin.json` is the Claude Code manifest, `plugin.json` is the Codex manifest, and `.claude-plugin/marketplace.json` lists the plugin for both apps. Skills live in `skills/<name>/SKILL.md` and reach the shared files at `../../shared/`. After you change `shared/study.py`, run:

```sh
python3 -m unittest discover -s shared
claude plugin validate .
```

To try a local change, add the repository folder as a marketplace: `claude plugin marketplace add ./` or `codex plugin marketplace add ./`, then install `english-study@english-study-skills`. To release, raise `version` in both manifests and push. `scripts/package.sh` builds `dist/english-study.zip` for apps that take a plugin as a zip file.

Still to verify:

- whether the Chat tab and Cowork in Claude Desktop can install the plugin and run `study.py` against the local study folder;
- whether a scheduled task that an agent writes to `~/.claude/scheduled-tasks/` shows up in Claude Desktop. Until then, the planner always prints the setup steps.

## License

MIT
