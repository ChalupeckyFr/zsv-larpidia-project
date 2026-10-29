"""Uloží neměnný snapshot atlasu do atlas/versions/<název>/.

Použití:
    python atlas/scripts/snapshot.py v0.1-outline --desc "Obrys A/B" --change "..." --change "..."

Do snapshotu se zkopíruje current/, docs/ a scripts/ (bez __pycache__), vznikne
MANIFEST.sha256 a SNAPSHOT.json. Existující snapshot se nikdy nepřepisuje.
Do atlas/CHANGELOG.md se připíše záznam.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from canon import ATLAS, bible_sha256, load_bible  # noqa: E402

PARTS = ("current", "docs", "scripts")


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("--desc", required=True)
    ap.add_argument("--change", action="append", default=[])
    ap.add_argument("--parent", default="")
    a = ap.parse_args()

    dest = ATLAS / "versions" / a.name
    if dest.exists():
        print(f"CHYBA: snapshot {a.name} už existuje a je neměnný.", file=sys.stderr)
        return 1
    dest.mkdir(parents=True)
    for part in PARTS:
        src = ATLAS / part
        if src.exists():
            shutil.copytree(src, dest / part, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))

    manifest = []
    for p in sorted(dest.rglob("*")):
        if p.is_file() and p.name not in ("MANIFEST.sha256", "SNAPSHOT.json"):
            manifest.append(f"{sha256_file(p)}  {p.relative_to(dest).as_posix()}")
    (dest / "MANIFEST.sha256").write_text("\n".join(manifest) + "\n", encoding="utf-8")

    now = dt.datetime.now().astimezone().isoformat(timespec="seconds")
    meta = {
        "name": a.name, "created": now, "description": a.desc, "changes": a.change,
        "parent": a.parent, "bible_version": load_bible()["meta"]["version"],
        "bible_sha256": bible_sha256(), "files": len(manifest),
    }
    (dest / "SNAPSHOT.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    log = ATLAS / "CHANGELOG.md"
    head = "# CHANGELOG atlasu Larpidie\n\nNejnovější nahoře. Každý záznam = neměnný snapshot ve `versions/`.\n\n"
    body = log.read_text(encoding="utf-8").split("\n\n", 2)[2] if log.exists() else ""
    entry = f"## {a.name} — {now[:10]}\n\n{a.desc}\n\n" + "".join(f"- {c}\n" for c in a.change) + "\n"
    log.write_text(head + entry + body, encoding="utf-8")
    print(f"Snapshot {a.name}: {len(manifest)} souborů → {dest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
