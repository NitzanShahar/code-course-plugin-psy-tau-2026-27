"""Build the Gemini packages from content/.

For each language: dist/gemini/<lang>/instructions.md (paste into a Gem's Instructions or a
Gemini Notebook's chat settings) and one knowledge file per chapter (<NN>-<slug>.md, upload to
Drive / the Gem / the Notebook). A Gem holds at most 10 knowledge files, so: one file per chapter.

Run: python tools/build_gemini.py
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LANGUAGES = {"r": "R", "python": "Python", "general": "General"}


def read(path):
    """Return (front matter dict, body) of a content file."""
    text = path.read_text(encoding="utf-8")
    match = re.match(r"---\n(.*?)\n---\n?(.*)", text, re.S)
    meta = dict(line.split(": ", 1) for line in match.group(1).splitlines())
    return meta, match.group(2).strip()


def main():
    template = (ROOT / "shared/gemini-instructions-template.md").read_text(encoding="utf-8")
    constitution = (ROOT / "shared/constitution.md").read_text(encoding="utf-8").strip()
    for lang_dir, language in LANGUAGES.items():
        src = ROOT / "content" / lang_dir
        if not src.exists():
            continue
        out = ROOT / "dist/gemini" / lang_dir
        out.mkdir(parents=True, exist_ok=True)
        for old in out.glob("*.md"):
            old.unlink()
        index, n_units = [], 0
        for chapter_dir in sorted(p for p in src.iterdir() if p.is_dir()):
            chapter, _ = read(chapter_dir / "chapter.md")
            number = int(chapter["id"].split("-")[1])
            index.append(f"**פרק {number} · {chapter['title']}**")
            sections = [f"# {language} · פרק {number}: {chapter['title']}"]
            for unit_file in sorted(chapter_dir.glob("[0-9]*.md")):
                unit, body = read(unit_file)
                shortcut = f"{number}.{int(unit['id'][-2:])}"
                index.append(f"- {shortcut} · {unit['title']}")
                sections.append(f"## יחידה {shortcut} · {unit['title']}\n\n{body}")
                n_units += 1
            index.append("")
            (out / f"{chapter_dir.name}.md").write_text("\n\n---\n\n".join(sections) + "\n",
                                                        encoding="utf-8", newline="\n")
        instructions = template.format(language=language, index="\n".join(index).strip(),
                                       constitution=constitution)
        (out / "instructions.md").write_text(instructions, encoding="utf-8", newline="\n")
        print(f"{language}: {n_units} units, instructions {len(instructions)} characters")


if __name__ == "__main__":
    main()
