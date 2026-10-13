# code-course-plugin-psy-tau-2026-27

AI tutor plugins for the TAU School of Psychology code courses: **R Course** and **Python Course**.
Each plugin holds the course's chapters and units; the student picks a unit and ChatGPT
teaches it step by step, following the course's teaching rules.

## How students use it
- **By chapter:** type `@R c`, pick a chapter from the dropdown (e.g. *R Course: Ch 02 · Atomic objects*),
  send. The chapter's units appear; write a unit number (e.g. `2.2`) to start.
- **By week:** pick *R Course* itself. It asks which week, then lists that week's units across chapters.

## Current status: test build (v0.5)

Each plugin has 2 chapters with 2 units. Checklist (free ChatGPT account, desktop app; update the plugins first):
1. **Labels.** `@R c` shows *R Course*, *Ch 01 · Interface*, *Ch 02 · Atomic objects*, with Hebrew descriptions.
2. **Chapter.** Select *Ch 02*, send with no text. Expect a bulleted unit list (no table) and a one-line prompt.
3. **Unit.** Write `2.2`. Expect the unit header, then step-by-step teaching. `חזור` returns to the list.
4. **Week view.** Select *R Course*, send with no text. Expect "which week?", then `1` lists all four units by chapter.
5. **Unprompted use.** New chat without `@`: `explain numeric objects in R`. A normal answer or a one-line question is fine.
6. **Python.** Repeat 1–4 with `@Python c`.
7. **RTL.** Hebrew reads right to left; code stays in code blocks.

## For TAs: adding or editing a unit
1. Edit or add a file in `plugins/<r|python>-course/units/<chapter>/` (copy an existing unit's front matter).
2. Run `python build.py`.
3. Commit and push. Students update the plugin from ChatGPT's Plugins page.
