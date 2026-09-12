#!/usr/bin/env python3
"""Validate distributable configuration and local skill references."""

import json
from pathlib import Path
import re
import tomllib

from install import validate_manifest


def main():
    root = Path(__file__).resolve().parents[1]
    manifest = json.loads((root / "manifest.json").read_text())
    validate_manifest(manifest, root)
    names = {entry["name"] for entry in manifest["skills"]}
    for entry in manifest["skills"]:
        if entry["kind"] != "local":
            continue
        path = root / entry["path"] / "SKILL.md"
        text = path.read_text()
        if not text.startswith("---\n"):
            raise ValueError(f"missing frontmatter: {path}")
        frontmatter = text.split("---", 2)[1]
        if not re.search(r"^name: " + re.escape(entry["name"]) + r"$", frontmatter, re.M) or not re.search(r"^description: .+", frontmatter, re.M):
            raise ValueError(f"invalid skill metadata: {path}")
        if "disable-model-invocation:" in frontmatter:
            raise ValueError(f"unsupported invocation metadata: {path}")
        for relative in re.findall(r"\.\./([a-z0-9-]+)/SKILL\.md", text):
            if relative not in names:
                raise ValueError(f"undeclared skill reference: {relative}")
        prose = re.sub(r"^```[^\n]*\n.*?^```[ \t]*$", "", text, flags=re.M | re.S)
        for reference in re.findall(r"\]\(([^)]+)\)", prose):
            if "://" not in reference and not reference.startswith("#") and not (path.parent / reference.split("#")[0]).exists():
                raise ValueError(f"broken reference {reference} in {path}")
    for entry in manifest["agents"]:
        role = tomllib.loads((root / entry["path"]).read_text())
        if role.get("name") != entry["name"] or not role.get("description") or not role.get("developer_instructions"):
            raise ValueError(f"invalid role {entry['name']}")
    print(f"Validated {len(names)} skills and {len(manifest['agents'])} roles. Runtime discovery is a separate smoke check.")


if __name__ == "__main__":
    main()
