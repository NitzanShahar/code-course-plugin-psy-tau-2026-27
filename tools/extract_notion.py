"""Extract the course units from the public Notion site into content/.

One Notion chapter page = one chapter; each top-level collapsible heading on it = one unit.
Units are written as content/<lang>/<NN-chapter>/<NN>.md with front matter (id, title).
content/<lang>/ids.json pins every Notion block to its unit id, so ids never change when
units are added or reordered in Notion (new units get the next free number).

Run:  python tools/extract_notion.py            (all languages)
      python tools/extract_notion.py R:1,2      (only R chapters 1 and 2)
"""

import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = "https://relic-collarbone-9bf.notion.site/api/v3/syncRecordValuesMain"

# language prefix -> list of (chapter slug, Notion page id); chapter number = position + 1
CHAPTERS = {
    "R": [
        ("interface", "1d0dccfed0598181b251eab3c1a9ab4b"),
        ("atomic-objects", "1d0dccfed059819cbf22dec2f330e18c"),
        ("vectors-matrices", "1d0dccfed0598142a090fde064c7130a"),
        ("data-structures", "1d0dccfed0598178b243ffc34a0c2b1e"),
        ("sampling", "1d0dccfed0598117b762c477f44ed3c2"),
        ("graphics", "1d0dccfed05981289360c8eb33f584cc"),
        ("anova", "1d0dccfed05981049cc4db9a4671152d"),
        ("regression", "1d0dccfed05981c8b063e823436c06dc"),
        ("flow-control", "1d0dccfed0598175b194c8ebfc61ea95"),
        ("functions-debugging", "1d0dccfed0598161b43ad06d0cf99202"),
    ],
    "PY": [
        ("intro", "1dbdccfed059810a9498e66bb8dbaaa1"),
        ("basic-objects", "1dbdccfed0598136ac63fb792fd4c1df"),
        ("vectors-matrices", "1dbdccfed0598154a98fe5cc6a7c21fb"),
        ("pandas", "1dbdccfed059810aba1bc003239313e2"),
        ("graphics", "1dbdccfed059815f9d11e4d70c5f5238"),
        ("models", "1dbdccfed059818bb9f1f6910487b1f7"),
        ("version-control", "1dbdccfed05981299693d167f2ceb7d1"),
        ("api", "1dbdccfed0598123b68dd64bc0811dab"),
        ("flow-control", "1dbdccfed05981f5b943c68b539b7109"),
        ("functions-debugging", "1dbdccfed05981baaa04ed86124f6160"),
    ],
    "GEN": [
        ("coding-guidelines", "26fdccfed05980a7b524f7f2a63a580d"),
        ("version-control", "1d0dccfed05981998dc0eb0a90473ea5"),
    ],
}
LANG_DIR = {"R": "r", "PY": "python", "GEN": "general"}

cache = {}


def uuid(hex_id):
    h = hex_id.replace("-", "")[-32:]
    return f"{h[:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:]}"


def fetch(ids):
    need = [i for i in dict.fromkeys(ids) if i not in cache]
    for k in range(0, len(need), 80):
        chunk = need[k:k + 80]
        body = {"requests": [{"pointer": {"table": "block", "id": i}, "version": -1} for i in chunk]}
        req = urllib.request.Request(API, data=json.dumps(body).encode(),
                                     headers={"content-type": "application/json", "user-agent": "Mozilla/5.0"})
        blocks = json.load(urllib.request.urlopen(req))["recordMap"].get("block", {})
        for i in chunk:
            value = (blocks.get(i) or {}).get("value")
            cache[i] = value.get("value", value) if isinstance(value, dict) else None
    return [cache[i] for i in ids]


def rich_text(title):
    out = []
    for part in title or []:
        text, marks = part[0] or "", part[1] if len(part) > 1 else []
        if text == "‣":  # inline mention of a page/user – no readable text
            continue
        kinds = {m[0]: (m[1] if len(m) > 1 else True) for m in marks}
        if "c" in kinds:
            text = f"`{text}`"
        elif "b" in kinds and text.strip():
            text = f"**{text.strip()}** "
        if "a" in kinds and kinds["a"] != text:
            text = f"{text} ({kinds['a']})"
        out.append(text)
    return "".join(out)


def tree(block_id, root=False):
    block = fetch([block_id])[0]
    if not block or block.get("alive") is False:
        return None
    if block["type"] == "transclusion_reference":  # synced block copy -> its original
        ref = block.get("format", {}).get("transclusion_reference_pointer", {}).get("id")
        return tree(ref) if ref else None
    props = block.get("properties", {})
    node = {
        "id": block_id,
        "type": block["type"],
        "text": rich_text(props.get("title")),
        "toggle": block["type"] == "toggle" or bool(block.get("format", {}).get("toggleable")),
        "lang": (props.get("language") or [[""]])[0][0],
        "src": (props.get("source") or props.get("link") or [[None]])[0][0],
        "children": [],
    }
    content = block.get("content") or []
    if content and (block["type"] != "page" or root):
        fetch(content)
        node["children"] = [n for n in (tree(c) for c in content) if n]
    return node


def unwrap(nodes):
    out = []
    for n in nodes:
        if n["type"] in ("transclusion_container", "column_list", "column"):
            out += unwrap(n["children"])
        else:
            out.append(n)
    return out


def to_markdown(nodes, indent=""):
    parts = []
    for n in unwrap(nodes):
        t, kids = n["text"], n["children"]
        sub = to_markdown(kids, indent + "  ") if kids else ""
        typ = n["type"]
        if typ in ("callout", "quote"):  # the prompt boxes: keep their content as plain text
            parts.append("\n\n".join(s for s in (t, to_markdown(kids, indent)) if s.strip()))
        elif typ == "text":
            parts.append(indent + t + ("\n" + sub if sub else ""))
        elif typ in ("bulleted_list", "to_do"):
            parts.append(f"{indent}- {t}" + ("\n" + sub if sub else ""))
        elif typ == "numbered_list":
            parts.append(f"{indent}1. {t}" + ("\n" + sub if sub else ""))
        elif typ == "code":
            lang = "" if n["lang"].lower() == "plain text" else n["lang"].lower()
            parts.append(f"```{lang}\n{t.strip('`')}\n```")
        elif typ in ("header", "sub_header", "sub_sub_header", "toggle"):
            parts.append(f"**{t.replace('**', '').strip()}**" + ("\n\n" + to_markdown(kids, indent) if kids else ""))
        elif typ in ("bookmark", "embed") and n["src"]:
            parts.append(f"קישור: {n['src']}")
        elif typ == "video" and n["src"] and re.match(r"https?://(www\.)?(youtube|youtu\.be|vimeo)", n["src"]):
            parts.append(f"סרטון: {n['src']}")
        elif typ in ("divider", "image", "file", "page", "video", "bookmark", "embed"):
            continue
        elif t:
            parts.append(indent + t)
    md = "\n\n".join(p for p in parts if p.strip())
    return re.sub(r"\n{3,}", "\n\n", re.sub(r"[ \t]+\n", "\n", md)).strip()


def extract(prefix, only=None):
    lang_dir = ROOT / "content" / LANG_DIR[prefix]
    ids_file = lang_dir / "ids.json"
    ids = json.loads(ids_file.read_text(encoding="utf-8")) if ids_file.exists() else {}
    for number, (slug, page_id) in enumerate(CHAPTERS[prefix], 1):
        if only and number not in only:
            continue
        page = tree(uuid(page_id), root=True)
        chapter_id = f"{prefix}-{number:02d}"
        chapter_dir = lang_dir / f"{number:02d}-{slug}"
        chapter_dir.mkdir(parents=True, exist_ok=True)
        (chapter_dir / "chapter.md").write_text(
            f"---\nid: {chapter_id}\ntitle: {page['text'].strip()}\n---\n", encoding="utf-8", newline="\n")
        units = [u for u in unwrap(page["children"]) if u["toggle"]]
        for unit in units:
            body = to_markdown(unit["children"])
            if len(body) < 30:  # empty placeholder heading in Notion
                continue
            if unit["id"] not in ids:
                taken = [int(v[-2:]) for v in ids.values() if v.startswith(chapter_id + "-")]
                ids[unit["id"]] = f"{chapter_id}-{max(taken, default=0) + 1:02d}"
            uid = ids[unit["id"]]
            title = unit["text"].replace("**", "").strip()
            (chapter_dir / f"{uid[-2:]}.md").write_text(
                f"---\nid: {uid}\ntitle: {title}\n---\n\n{body}\n", encoding="utf-8", newline="\n")
        print(f"{chapter_id} {page['text'].strip()}: {len(units)} units")
    ids_file.write_text(json.dumps(ids, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        prefix, _, nums = sys.argv[1].partition(":")
        extract(prefix, {int(n) for n in nums.split(",")} if nums else None)
    else:
        for prefix in CHAPTERS:
            extract(prefix)
