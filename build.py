"""Build the course plugins from their sources.

Sources (edit these):  shared/constitution.md, shared/skill-template.md,
                       plugins/<plugin>/units/**, PLUGINS / VERSION below.
Generated (never edit): plugins/<plugin>/{plugin.json, .codex-plugin/plugin.json,
                       catalog.json, skills/**},
                       .agents/plugins/marketplace.json

Run: python build.py
"""

import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
VERSION = "0.8.0"
PLUGINS = {
    "r-course": {"language": "R", "prefix": "R", "display": "R-Course"},
    "python-course": {"language": "Python", "prefix": "PY", "display": "Python-Course"},
}


def front_matter(path):
    """Parse the simple `key: value` front matter at the top of a markdown file."""
    text = path.read_text(encoding="utf-8")
    match = re.match(r"---\n(.*?)\n---", text, re.S)
    if not match:
        raise ValueError(f"{path}: missing front matter")
    meta = {}
    for line in match.group(1).splitlines():
        key, _, value = line.partition(":")
        value = value.strip()
        if value.startswith("["):
            value = [int(v) for v in value.strip("[]").split(",") if v.strip()]
        meta[key.strip()] = value
    return meta


def unit_body(path):
    """A unit file's text without its front matter."""
    return re.sub(r"\A---\n.*?\n---\n", "", path.read_text(encoding="utf-8"), flags=re.S).strip()


def no_spaces(path, name):
    """name_en becomes part of dropdown labels and skill names: letters, digits and hyphens only."""
    if not re.fullmatch(r"[A-Za-z0-9-]+", name):
        raise ValueError(f"{path}: name_en '{name}' must use only letters, digits and hyphens")
    return name


def build_catalog(plugin_dir, cfg):
    chapters, seen = [], set()
    for chapter_dir in sorted(p for p in (plugin_dir / "units").iterdir() if p.is_dir()):
        chapter = front_matter(chapter_dir / "chapter.md")
        units = []
        for unit_file in sorted(chapter_dir.glob("[0-9]*.md")):
            unit = front_matter(unit_file)
            uid = unit["id"]
            if not re.fullmatch(rf"{cfg['prefix']}-\d\d-\d\d", uid) or not uid.startswith(chapter["id"] + "-"):
                raise ValueError(f"{unit_file}: id {uid} does not match chapter {chapter['id']}")
            if uid in seen:
                raise ValueError(f"{unit_file}: duplicate id {uid}")
            seen.add(uid)
            _, ch, un = uid.split("-")
            units.append({
                "id": uid,
                "shortcut": f"{int(ch)}.{int(un)}",
                "title": unit["title"],
                "name_en": no_spaces(unit_file, unit["name_en"]),
                "path": unit_file.relative_to(plugin_dir).as_posix(),
            })
        chapters.append({
            "id": chapter["id"],
            "number": int(chapter["id"].split("-")[1]),
            "title": chapter["title"],
            "name_en": no_spaces(chapter_dir / "chapter.md", chapter["name_en"]),
            "units": units,
        })
    return {"plugin": plugin_dir.name, "language": cfg["language"], "chapters": chapters}


def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not isinstance(content, str):
        content = json.dumps(content, ensure_ascii=False, indent=2) + "\n"
    path.write_text(content, encoding="utf-8", newline="\n")


def manifest(name, cfg):
    return {
        "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
        "name": name,
        "version": VERSION,
        "description": f"TAU Psychology {cfg['language']} course tutor: choose a chapter and unit, "
                       f"and learn it step by step. When mentioned, read the {name} skill and show its menu.",
        "author": {"name": "Nitzan Shahar"},
        "license": "MIT",
        "keywords": ["education", cfg["language"], "tutor"],
        "extensions": {"com.openai": {"interface": {
            "displayName": cfg["display"],
            "shortDescription": f"קורס {cfg['language']} – יחידות לימוד עם מתרגל AI",
            "category": "Education",
            "defaultPrompt": ["פתח את תפריט הקורס"],
        }}},
    }


def main():
    template = (ROOT / "shared/skill-template.md").read_text(encoding="utf-8")
    chapter_template = (ROOT / "shared/chapter-skill-template.md").read_text(encoding="utf-8")
    unit_template = (ROOT / "shared/unit-skill-template.md").read_text(encoding="utf-8")
    constitution = (ROOT / "shared/constitution.md").read_text(encoding="utf-8").strip()
    marketplace = []
    for name, cfg in PLUGINS.items():
        plugin_dir = ROOT / "plugins" / name
        catalog = build_catalog(plugin_dir, cfg)
        write(plugin_dir / "catalog.json", catalog)
        shutil.rmtree(plugin_dir / "skills", ignore_errors=True)  # skills are fully generated

        def add_skill(skill, content, label, description):
            write(plugin_dir / "skills" / skill / "SKILL.md", content)
            write(plugin_dir / "skills" / skill / "agents/openai.yaml",
                  f'interface:\n  display_name: "{label}"\n  short_description: "{description}"\n')

        # Skills are self-contained: menus, unit text and constitution are pasted in,
        # so ChatGPT never has to open another file (faster, and works in Chat mode).
        def menu(chapter):
            lines = [f"**פרק {chapter['number']} · {chapter['title']}**", ""]
            lines += [f"- **{u['shortcut']}** · {u['title']}" for u in chapter["units"]]
            return "\n".join(lines)

        index = "\n\n".join([f"**ספריית היחידות · {cfg['language']}**"] + [menu(c) for c in catalog["chapters"]])
        add_skill(name, template.format(plugin=name, index=index, **cfg), cfg["display"], "כל הפרקים והיחידות")
        prefix = cfg["prefix"].lower()
        for chapter in catalog["chapters"]:
            ch = f"ch{chapter['number']:02d}"
            units_text = "\n\n".join(
                f"### יחידה {u['shortcut']} · {u['title']}\n\n{unit_body(plugin_dir / u['path'])}"
                for u in chapter["units"])
            chapter_menu = menu(chapter) + f"\n\nכתבו את מספר היחידה כדי להתחיל, למשל {chapter['units'][0]['shortcut']}."
            skill = f"{prefix}-{ch}-{chapter['name_en'].lower()}"
            add_skill(skill, chapter_template.format(
                skill=skill, language=cfg["language"], display=cfg["display"],
                number=chapter["number"], title=chapter["title"], name_en=chapter["name_en"],
                first_shortcut=chapter["units"][0]["shortcut"], menu=chapter_menu,
                units=units_text, constitution=constitution),
                f"Ch{chapter['number']:02d}-{chapter['name_en']}", chapter["title"])
            for unit in chapter["units"]:
                skill = f"{prefix}-{ch}-u{unit['id'][-2:]}-{unit['name_en'].lower()}"
                add_skill(skill, unit_template.format(
                    skill=skill, language=cfg["language"], display=cfg["display"],
                    unit_body=unit_body(plugin_dir / unit["path"]), constitution=constitution, **unit),
                    f"Ch{chapter['number']:02d}-{unit['shortcut']}-{unit['name_en']}", unit["title"])
        write(plugin_dir / "plugin.json", manifest(name, cfg))
        write(plugin_dir / ".codex-plugin/plugin.json", {**manifest(name, cfg), "skills": "./skills/"})
        marketplace.append({
            "name": name,
            "source": {"source": "local", "path": f"./plugins/{name}"},
            "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
            "category": "Education",
        })
        n_units = sum(len(c["units"]) for c in catalog["chapters"])
        print(f"{name}: {len(catalog['chapters'])} chapters, {n_units} units")
    write(ROOT / ".agents/plugins/marketplace.json", {
        "name": "tau-psy-code-course",
        "interface": {"displayName": "TAU Psychology – Code Courses"},
        "plugins": marketplace,
    })


if __name__ == "__main__":
    main()
