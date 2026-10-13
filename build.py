"""Build the course plugins from their sources.

Sources (edit these):  shared/constitution.md, shared/skill-template.md,
                       plugins/<plugin>/units/**, PLUGINS / VERSION below.
Generated (never edit): plugins/<plugin>/{plugin.json, .codex-plugin/plugin.json,
                       catalog.json, shared/constitution.md, skills/<plugin>/**},
                       .agents/plugins/marketplace.json

Run: python build.py
"""

import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
VERSION = "0.5.0"
PLUGINS = {
    "r-course": {"language": "R", "prefix": "R", "display": "R Course"},
    "python-course": {"language": "Python", "prefix": "PY", "display": "Python Course"},
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
                "weeks": unit.get("weeks", []),
                "path": unit_file.relative_to(plugin_dir).as_posix(),
            })
        chapters.append({
            "id": chapter["id"],
            "number": int(chapter["id"].split("-")[1]),
            "title": chapter["title"],
            "name_en": chapter["name_en"],
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
    marketplace = []
    for name, cfg in PLUGINS.items():
        plugin_dir = ROOT / "plugins" / name
        catalog = build_catalog(plugin_dir, cfg)
        write(plugin_dir / "catalog.json", catalog)
        (plugin_dir / "shared").mkdir(exist_ok=True)
        shutil.copyfile(ROOT / "shared/constitution.md", plugin_dir / "shared/constitution.md")
        skill_dir = plugin_dir / "skills" / name
        write(skill_dir / "SKILL.md", template.format(plugin=name, **cfg))
        write(skill_dir / "agents/openai.yaml",
              f'interface:\n  display_name: "{cfg["display"]}"\n'
              f'  short_description: "Weekly view – choose your week"\n')
        for chapter in catalog["chapters"]:
            folder = Path(chapter["units"][0]["path"]).parent.name
            skill = f"{cfg['prefix'].lower()}-{folder}"
            write(plugin_dir / "skills" / skill / "SKILL.md", chapter_template.format(
                skill=skill, language=cfg["language"], display=cfg["display"],
                number=chapter["number"], title=chapter["title"], name_en=chapter["name_en"],
                chapter_id=chapter["id"], first_shortcut=chapter["units"][0]["shortcut"]))
            write(plugin_dir / "skills" / skill / "agents/openai.yaml",
                  f'interface:\n  display_name: "Ch {chapter["number"]:02d} · {chapter["name_en"]}"\n'
                  f'  short_description: "{chapter["title"]}"\n')
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
