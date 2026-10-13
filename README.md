# code-course-plugin-psy-tau-2026-27

AI tutor plugins for the TAU School of Psychology code courses: **R Course** and **Python Course**.
Each plugin holds the course's chapters and units; the student picks a unit and ChatGPT
teaches it step by step, following the course's teaching rules.

## How students use it
Type `@R-C` (or `@Python-C`) and pick from the dropdown – every entry starts right away:
- `R-Course` – the whole library: all chapters and units.
- `R-Course: Ch02-Atomic-objects` – that chapter's units.
- `R-Course: Ch02-2.2-Numeric` – that unit.

Typing more filters the list, e.g. `@R-C ch02` or `@R-C numeric`.

## Current status: test build (v0.7)

Each plugin has 2 chapters with 2 units, each as its own dropdown entry.
Checklist (free ChatGPT account, desktop app; update or reinstall the plugins first):
1. **Labels.** `@R-C` lists *R-Course*, *Ch01-Interface*, *Ch01-1.1-History*, … with Hebrew descriptions.
2. **Filter.** Does `@R-C ch02` show only chapter 2 and its units? Does `@R-C numeric` find unit 2.2?
3. **Unit.** Select *Ch02-2.2-Numeric*, send with no text. The unit should start immediately.
4. **Chapter.** Select *Ch02-Atomic-objects*, send with no text. Expect its unit list.
5. **Library.** Select *R-Course*, send with no text. Expect all chapters and units.
6. **Unprompted use.** New chat without `@`: `explain numeric objects in R`. Note what happens.
7. **Python.** Repeat 1–3 with `@Python-C`.

## For TAs: adding or editing a unit
1. Edit or add a file in `plugins/<r|python>-course/units/<chapter>/` (copy an existing unit's front matter).
2. Run `python build.py`.
3. Commit and push. Students update the plugin from ChatGPT's Plugins page.
