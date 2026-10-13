# code-course-plugin-psy-tau-2026-27

AI tutor plugin for the TAU School of Psychology code courses (R, Python).
Each chapter is a skill; each unit is a prompt file the skill runs with the student.

## Current status: test build

`plugins/code-course-test` contains one chapter (R · 02 atomic objects) with three units.
It exists to answer four questions before we build the full library.

```
.agents/plugins/marketplace.json          ← marketplace entry pointing to the plugin
plugins/code-course-test/
  plugin.json                             ← manifest (portable layout)
  .codex-plugin/plugin.json               ← same manifest (compatibility layout)
  shared/constitution.md                  ← course-wide teaching rules (Option A)
  units/r/02-atomic-objects/*.md          ← unit prompts (Option A)
  skills/r-02-atomic-objects/
    SKILL.md                              ← menu + orchestration
    agents/openai.yaml                    ← disables automatic invocation
    references/*.md                       ← copies of the above (Option B fallback)
```

## Test checklist (run with a FREE ChatGPT account, desktop app)

1. **Install.** Add this repository as a plugin marketplace and install `code-course-test`
   from the Plugins Directory. Record exactly which steps/menus were needed.
   Codex CLI equivalent: `codex plugin marketplace add NitzanShahar/code-course-plugin-psy-tau-2026-27`
2. **Unprompted use.** In a new chat, write *"explain numeric objects in R"* without `@`
   and note whether the plugin starts by itself. (v0.1 used `allow_implicit_invocation: false`;
   it stopped the skill from loading at all inside a plugin, so v0.2 removed it.)
3. **Deliberate invocation.** Type `@code-course-test` plus any text. The first line should be
   `[בדיקה] חוקת הקורס נטענה מתוך: ...` — record whether it says the plugin-level shared
   folder (Option A works) or the skill references copy (Option B needed).
4. **Unit loop.** Choose unit 2. Check: one step at a time, waits for you, hints without code
   on wrong practice code, solution only on request, menu returns at the end.
   Also try `@r-02-atomic-objects 3` to confirm the menu is skipped.
