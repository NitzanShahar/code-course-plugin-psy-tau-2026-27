# code-course-plugin-psy-tau-2026-27

AI tutor plugins for the TAU School of Psychology code courses: **R Course** and **Python Course**.
Each plugin holds the course's chapters and units; the student picks a unit and ChatGPT
teaches it step by step, following the course's teaching rules.

## Current status: test build (v0.4)

Each plugin has 2 chapters with 2 units. v0.4 adds one skill per chapter next to the main
skill, to test whether ChatGPT's picker lets students select a chapter directly.

## Picker test (v0.4)

Update the plugins first (Plugins → Installed, or reinstall). Then note what appears in each case:
1. Type `@R course` and look at the dropdown **before** pressing Tab. One entry, or three
   (`r-course`, `r-01-interface`, `r-02-atomic-objects`)?
2. Type `$` alone. Is there a list? Does it show the plugin's skills?
3. Type `$r-course:`. Does it list the chapter skills?
4. If a chapter skill can be selected: send it with no text. Expect that chapter's unit menu.

## Menu flow checklist (v0.3, still valid)

1. **Install.** Uninstall the old `code-course-test`. Add this repo as a marketplace again (or refresh it)
   and install **R Course** and **Python Course**.
2. **Chapter menu.** New chat: `@R Course` + `פתח את התפריט`. Expect two chapters as a list (no table).
3. **Unit menu.** Reply `2`. Expect units `2.2` and `2.3`, each with its week.
4. **Shortcut.** New chat: `@R Course 1.2`. Expect the installation unit to start directly.
5. **Week view.** `שבוע 1` should list all four units, grouped by chapter.
6. **Next.** Finish a unit, then `הבא`. After `1.2` it should continue to `2.2`.
7. **Unprompted use.** New chat without `@`: `explain numeric objects in R`.
   Expect a one-line question whether you want a course unit.
8. **Python.** Repeat 2–4 with `@Python Course`.
9. **RTL.** All Hebrew lines read right to left; code stays in code blocks.

## For TAs: adding or editing a unit
1. Edit or add a file in `plugins/<r|python>-course/units/<chapter>/` (copy an existing unit's front matter).
2. Run `python build.py`.
3. Commit and push. Students update the plugin from ChatGPT's Plugins page.
