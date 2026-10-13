# Code course plugin – project notes

ChatGPT plugins that tutor TAU Psychology students in R and Python, using the unit
prompts the course team wrote (source: the course Notion site).
Target: students on **free** ChatGPT accounts, desktop app.

## Source content
Notion chapter pages (one collapsible heading = one unit): R 72 units / 10 chapters,
Python 75 / 10, general (coding guidelines, version control) 9 – maybe a third plugin.
Index pages: R https://relic-collarbone-9bf.notion.site/R-1d0dccfed05981b686adec370d61a3cf ,
Python https://relic-collarbone-9bf.notion.site/Python-1dbdccfed05980488e62cf7d132ef143 ,
general https://relic-collarbone-9bf.notion.site/26fdccfed05980a7b241c2b2472b2c9f .
Units sit in synced blocks; the public API `/api/v3/syncRecordValuesMain` reads them.

## Structure
```
shared/constitution.md          teaching rules for every unit (edit here only)
shared/skill-template.md        main skill per plugin = library index (edit here only)
shared/chapter-skill-template.md  one skill per chapter: its unit list (edit here only)
shared/unit-skill-template.md   one skill per unit: starts it directly (edit here only)
plugins/<r|python>-course/
  units/<NN-chapter>/chapter.md     chapter id, Hebrew title, English name_en
  units/<NN-chapter>/<NN-unit>.md   one unit = one prompt; front matter id, title, name_en
  (everything else in the plugin is generated)
build.py                        generates manifests, catalog.json, all skills + their
                                agents/openai.yaml labels, .agents/plugins/marketplace.json
                                Skills are self-contained: build pastes menus, unit text
                                and the constitution into each SKILL.md (no file reads).
```
After any edit: `python build.py`, then commit the generated files too.

## Conventions
- The plugin is a prompt library: no weeks, schedules or "what's next" logic.
  Students know which chapter and unit to do; the plugin only makes units easy to reach.
- `name_en` builds the dropdown labels (`R-Course: Ch02-2.2-Numeric`): letters, digits,
  hyphens only – no spaces anywhere in labels or skill names (build.py enforces it).
- Unit front matter: `id`, `title`, `name_en`. IDs are permanent
  (`R-02-03`, `PY-02-03`); never renumber. Shortcut `2.3` is derived from the id.
- Unit text stays in the TAs' Hebrew wording, in the student's voice ("explain to me").
  Drop embedded video files; keep links.
- Menus are generated from `catalog.json`, never written by hand. This keeps a
  future clickable menu (an app/MCP view sending a unit id) compatible.

## What we verified in ChatGPT (free account, desktop, Oct 2026)
- A plugin installs from this public GitHub repo via its marketplace file.
- Typing `@R c` or `$r-course:` lists **every skill in the plugin** (shown as
  `$plugin:skill`). So the dropdown is the clickable menu: one plugin per language,
  with skills for the whole library, each chapter, and each unit.
  Selecting a skill with no text still starts it.
- Dropdown labels come from each skill's `agents/openai.yaml` (`display_name`,
  `short_description`); without it ChatGPT shows the raw name and description.
  Keep `display_name` English (mixed Hebrew/English lines get scrambled);
  the Hebrew title goes in `short_description`.
- Zero-padded chapter numbers keep the dropdown in order.
- `allow_implicit_invocation: false` stopped the skill from loading at all inside a
  plugin (ChatGPT saw only the description and invented a menu). Do not use it.
- In Work mode a skill can read plugin-level files, but that cost >1 min of agent work
  per unit and used up the free account's **Work/Codex quota** after a few tests.
  Free accounts have unlimited everyday Chat, so skills must stay cheap: self-contained,
  no file reads. Still to verify: that plugin skills run in Chat mode.
- The unfiltered dropdown is not sorted; filtering (`@R-C ch02`) works and sorts it out.
- ChatGPT may use the plugin unprompted; the skill asks first in that case.
- Hebrew: tables break in RTL – use lists; the constitution states this.
- Custom GPTs are retired Dec 2026; plugins replace them. Standalone skills are
  paid-only, so plugins are the only route for free accounts.
