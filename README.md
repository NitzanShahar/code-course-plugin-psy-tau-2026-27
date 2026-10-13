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

## Current status: test build (v0.8)

v0.7 confirmed the dropdown (labels, filtering, starting a unit). But it ran in **Work mode**,
which on a free account has a small quota that ran out. v0.8 makes every skill self-contained
(no file reads), so it should be faster and lighter.

Checklist (free account, desktop app; update or reinstall the plugins first):
1. **Chat mode.** Switch the composer from *Work* to normal *Chat*. Does `@R-C` still show the list?
2. **Unit in Chat mode.** Select `Ch02-2.2-Numeric`, send with no text. Does the unit start? How long does it take?
3. **Chapter in Chat mode.** Select `Ch02-Atomic-objects`, send. Expect its unit list; then `2.3` starts that unit.
4. **Library.** Select `R-Course`, send. Expect all chapters and units.
5. **Usage.** After a few units, check whether any limit message appears, and for which meter (Chat or Work).

## For TAs: adding or editing a unit
1. Edit or add a file in `plugins/<r|python>-course/units/<chapter>/` (copy an existing unit's front matter).
2. Run `python build.py`.
3. Commit and push. Students update the plugin from ChatGPT's Plugins page.
