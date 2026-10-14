# Scheduling

Every scheduled run uses the same prompt. Replace `<days>` and `<time>`:

```
This is a scheduled run of my English study. Use the english-today skill: run `study status`, do the one step that is due, and end. The learner is not here right now, so the message you write is the lesson: make it complete, with every exercise in the chat.
```

Scheduled runs need the computer on and the app open. A run that was missed while the computer slept runs once when the app opens again (Claude Desktop) or is skipped.

## Claude Desktop

Scheduled tasks run locally in the Code tab and can read the study folder.

1. Open Claude Desktop, go to the **Code** tab, and choose **Scheduled** in the sidebar.
2. Click **New task**. Name: `English study`. Prompt: the text above.
3. Set the folder to the study folder (from `study where`) and the schedule to the learner's days and time.
4. Allow the task to run commands without asking, so it can run `study.py` while the learner is away.

If your tools include a scheduled-task tool (for example in Claude Desktop), offer to create the task with it after the learner agrees, and still show these steps.

Cowork scheduled tasks also work, but they run in the cloud and reach the study folder only while the desktop app is open. Tell the learner this if they use Cowork.

## Codex app

1. Open the Codex app and choose the study folder as the project.
2. Open **Scheduled tasks** and create a task with the prompt above, repeating on the learner's days at their time.
3. Keep the app running at that time, and allow network access for the task, because listening tasks fetch transcripts. Codex CLI has no scheduler; use the cron recipe below for it.

## cron or launchd (advanced users)

For Claude Code or Codex CLI on a computer that is always on. The lesson goes to a file in `inbox/` and a notification appears.

```
# crontab -e   (weekdays at 10:00)
0 10 * * 1-5 cd "$HOME/.english-study" && claude -p "<prompt above>" > "inbox/$(date +\%F).md" && osascript -e 'display notification "Your English lesson is ready" with title "English study"'
```

For Codex CLI, replace `claude -p "<prompt>"` with `codex exec -s workspace-write -c sandbox_workspace_write.network_access=true "<prompt>"`. Listening and pronunciation tasks need network access to fetch transcripts, and the default Codex sandbox has none. The learner opens the file in `inbox/` and answers in a normal chat with the agent: "here is my homework: ...".

## Manual use

Without a schedule the learner says "next lesson" or "let's study" in any chat; `english-today` works out what is due. Tell every learner this works, even with a schedule.
