#!/usr/bin/env python3
"""Install the manifest's named skills and agents without changing user config."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile
import tomllib
import urllib.error
import urllib.request


def relative_path(value):
    path = Path(value)
    if path.is_absolute() or ".." in path.parts or not path.parts:
        raise ValueError(f"expected a contained relative path: {value}")
    return path


def validate_manifest(spec, directory):
    if spec["version"] != 1:
        raise ValueError("unsupported manifest version")
    skill_names = set()
    for section in ("skills", "agents"):
        names = set()
        for entry in spec[section]:
            name = entry["name"]
            if not re.fullmatch(r"[a-z][a-z0-9_-]{0,63}", name) or name in names:
                raise ValueError(f"invalid or duplicate {section} name: {name}")
            names.add(name)
            if "path" in entry:
                source = directory / relative_path(entry["path"])
                if not source.resolve().is_relative_to(directory.resolve()):
                    raise ValueError(f"source escapes manifest directory: {source}")
                if source.is_symlink() or (source.is_dir() and any(p.is_symlink() for p in source.rglob("*"))):
                    raise ValueError(f"source contains a symlink: {source}")
            for file in entry.get("files", []):
                relative_path(file["path"])
                if not re.fullmatch(r"[a-f0-9]{64}", file["sha256"]):
                    raise ValueError(f"invalid SHA-256 for {name}")
            if section == "agents" and not set(entry["skills"]).issubset(skill_names):
                raise ValueError(f"undeclared required skill for {name}")
        if section == "skills":
            skill_names = names


def check_destination(target):
    for path in (target, *target.parents):
        if path.is_symlink():
            raise ValueError(f"destination contains a symlink: {path}")


def install(args):
    manifest = args.manifest.resolve()
    spec = json.loads(manifest.read_text())
    validate_manifest(spec, manifest.parent)
    root = (args.workspace or args.home).resolve()
    skill_root = root / ".agents/skills"
    codex_home = args.codex_home or Path(os.environ.get("CODEX_HOME", str(root / ".codex")))
    agent_root = (root / ".codex" if args.workspace else codex_home.resolve()) / "agents"
    with tempfile.TemporaryDirectory(prefix="codex-workflow-stage-") as temp:
        stage = Path(temp)
        pending = []
        for entry in spec["skills"]:
            source = stage / "skills" / entry["name"]
            if entry["kind"] == "local":
                shutil.copytree(manifest.parent / entry["path"], source)
            elif entry["kind"] == "upstream":
                for file in entry["files"]:
                    try:
                        with urllib.request.urlopen(file["url"], timeout=30) as response:
                            data = response.read()
                    except (OSError, urllib.error.URLError) as error:
                        raise ValueError(f"download failed for {entry['name']}/{file['path']}: {error}") from error
                    if hashlib.sha256(data).hexdigest() != file["sha256"]:
                        raise ValueError(f"SHA-256 mismatch for {entry['name']}/{file['path']}")
                    path = source / file["path"]
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_bytes(data)
            else:
                raise ValueError(f"unknown skill kind: {entry['kind']}")
            if not (source / "SKILL.md").is_file():
                raise ValueError(f"missing SKILL.md for {entry['name']}")
            pending.append((source, skill_root / entry["name"]))
        for entry in spec["agents"]:
            content = (manifest.parent / entry["path"]).read_text()
            content = content.replace("{{skills_root}}", json.dumps(str(skill_root), ensure_ascii=False)[1:-1])
            for name in entry["skills"]:
                content += '\n[[skills.config]]\npath = ' + json.dumps(str(skill_root / name / "SKILL.md")) + '\nenabled = true\n'
            role = tomllib.loads(content)
            if role.get("name") != entry["name"] or not role.get("description") or not role.get("developer_instructions"):
                raise ValueError(f"invalid custom agent: {entry['name']}")
            source = stage / "agents" / (entry["name"] + ".toml")
            source.parent.mkdir(parents=True, exist_ok=True)
            source.write_text(content)
            pending.append((source, agent_root / source.name))
        # Validate every destination before publishing any prepared files.
        for source, target in pending:
            check_destination(target)
            if target.exists() and source.is_dir() != target.is_dir():
                raise ValueError(f"destination has the wrong file type: {target}")
        for source, target in pending:
            target.parent.mkdir(parents=True, exist_ok=True)
            if source.is_dir():
                if target.exists():
                    shutil.rmtree(target)
                shutil.copytree(source, target)
            else:
                shutil.copyfile(source, target)
    print(f"Installed {len(spec['skills'])} skills and {len(spec['agents'])} agents into {root}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    scope = parser.add_mutually_exclusive_group(required=True)
    scope.add_argument("--workspace", type=Path)
    scope.add_argument("--global", dest="global_install", action="store_true")
    parser.add_argument("--home", type=Path, default=Path.home(), help="Global skill home, default: user's home")
    parser.add_argument("--codex-home", type=Path, help="Global agent home, default: CODEX_HOME or HOME/.codex")
    parser.add_argument("--manifest", type=Path, default=Path(__file__).resolve().parents[1] / "manifest.json")
    args = parser.parse_args()
    try:
        install(args)
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"Install failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
