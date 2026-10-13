# Code course plugin – project notes

ChatGPT plugins that tutor TAU Psychology students in R and Python, using the unit
prompts the course team wrote (source: the course Notion site, organized by week).
Target: students on **free** ChatGPT accounts, desktop app.

## Structure
```
shared/constitution.md          teaching rules for every unit (edit here only)
shared/skill-template.md        main skill per plugin = library index (edit here only)
shared/chapter-skill-template.md  one skill per chapter (edit here only)
plugins/<r|python>-course/
  units/<NN-chapter>/chapter.md     chapter id, Hebrew title, short English name_en
  units/<NN-chapter>/<NN-unit>.md   one unit = one prompt, with front matter
  (everything else in the plugin is generated)
build.py                        generates manifests, catalog.json, all skills + their
                                agents/openai.yaml labels, constitution copies,
                                .agents/plugins/marketplace.json
```
After any edit: `python build.py`, then commit the generated files too.

## Conventions
- The plugin is a prompt library: no weeks, schedules or "what's next" logic.
  Students know which chapter and unit to do; the plugin only makes units easy to reach.
- Unit front matter: `id`, `title`. IDs are permanent
  (`R-02-03`, `PY-02-03`); never renumber. Shortcut `2.3` is derived from the id.
- Unit text stays in the TAs' Hebrew wording, in the student's voice ("explain to me").
  Drop embedded video files; keep links.
- Menus are generated from `catalog.json`, never written by hand. This keeps a
  future clickable menu (an app/MCP view sending a unit id) compatible.

## What we verified in ChatGPT (free account, desktop, Oct 2026)
- A plugin installs from this public GitHub repo via its marketplace file.
- Typing `@R c` or `$r-course:` lists **every skill in the plugin** (shown as
  `$plugin:skill`). So the dropdown is the clickable chapter menu: one plugin per
  language, one skill per chapter, plus a main skill listing the whole library.
  Selecting a chapter skill with no text still starts it.
- Dropdown labels come from each skill's `agents/openai.yaml` (`display_name`,
  `short_description`); without it ChatGPT shows the raw name and description.
  Keep `display_name` English (mixed Hebrew/English lines get scrambled).
- Zero-padded chapter numbers keep the dropdown in order.
- `allow_implicit_invocation: false` stopped the skill from loading at all inside a
  plugin (ChatGPT saw only the description and invented a menu). Do not use it.
- The skill can read plugin-level files (`../../shared/…`, `../../units/…`).
- ChatGPT may use the plugin unprompted; the skill asks first in that case.
- Hebrew: tables break in RTL – use lists; the constitution states this.
- Custom GPTs are retired Dec 2026; plugins replace them. Standalone skills are
  paid-only, so plugins are the only route for free accounts.
