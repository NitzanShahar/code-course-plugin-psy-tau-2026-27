---
name: r-02-atomic-objects
description: R course tutor, chapter 2 – atomic objects. Use whenever the student mentions this plugin, even with no other text. Before replying, read this SKILL.md and its files – the unit menu and unit content exist only in these files; never invent unit names or content.
---

# R · Chapter 2: Atomic objects (אובייקטים בסיסיים)

## Step 1 – load the constitution (TEST BUILD: report where it came from)

Try to read `../../shared/constitution.md` (the plugin-level shared file).
- If that works, remember SOURCE = "plugin-level shared folder".
- If not, read `references/constitution.md` instead and remember SOURCE = "skill references copy".

Follow the constitution for the rest of the conversation.

## Step 2 – show the menu and wait

Begin your first message with this line (test build only):
`[בדיקה] חוקת הקורס נטענה מתוך: <SOURCE>`

Then show this menu, exactly, and ask the student which unit to start (by number):

| # | יחידה | שבוע |
|---|-------|------|
| 1 | מבוא לאובייקטים בסיסיים | 1 |
| 2 | אובייקט מספרי (numeric) | 1 |
| 3 | אובייקט מחרוזת (string) | 1 |

If the student already named a unit when invoking the skill (for example "2" or "numeric"),
skip the menu and go straight to Step 3.

## Step 3 – run the chosen unit

Unit files, by number:
1. `01-intro.md`
2. `02-numeric.md`
3. `03-string.md`

Read only the chosen file. Try `../../units/r/02-atomic-objects/<file>` first;
if that fails, read `references/<file>`.
On the first line of the unit (test build only) state which location the unit was read from.

Run the unit according to the constitution.

## Step 4 – after the unit

Say the unit is complete, then show the menu from Step 2 again (without the test line).
