#!/usr/bin/env python3
"""Install pinned upstream skills unchanged, plus this kit's skills and roles, for Codex and Claude Code."""

import argparse
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import sys
import tarfile
import tempfile
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ("codex", "claude")
NAME = re.compile(r"[a-z][a-z0-9_-]{0,63}")
RECORD = ".workflow-kit.json"


def archive_url(source):
    if "archive" in source:
        return source["archive"]
    repo = source["repository"].removeprefix("https://github.com/")
    return f"https://codeload.github.com/{repo}/tar.gz/{source['revision']}"


def fetch_upstream(source, stage):
    """Extract each listed skill directory byte-for-byte from the pinned archive."""
    url = archive_url(source)
    try:
        with urllib.request.urlopen(url, timeout=60) as response:
            data = response.read()
    except (OSError, urllib.error.URLError) as error:
        raise ValueError(f"download failed for {url}: {error}") from error
    wanted = {name: PurePosixPath(path) for name, path in source["skills"].items()}
    found = set()
    with tarfile.open(fileobj=io.BytesIO(data)) as archive:
        for member in archive.getmembers():
            parts = PurePosixPath(member.name).parts[1:]  # drop the archive's top-level directory
            for name, prefix in wanted.items():
                if parts[:len(prefix.parts)] != prefix.parts:
                    continue
                if member.issym() or member.islnk() or ".." in parts:
                    raise ValueError(f"unsafe archive entry for {name}: {member.name}")
                if member.isfile():
                    target = stage / name / Path(*parts[len(prefix.parts):])
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(archive.extractfile(member).read())
                    found.add(name)
    for name in wanted:
        if name not in found or not (stage / name / "SKILL.md").is_file():
            raise ValueError(f"{name} not found at {source['skills'][name]} in {url}")


def parse_role(path):
    text = path.read_text()
    match = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S)
    if not match:
        raise ValueError(f"missing frontmatter: {path}")
    meta = {}
    for line in match.group(1).splitlines():
        key, _, value = line.partition(":")
        value = value.strip()
        if value.startswith("[") and value.endswith("]"):
            value = [item.strip() for item in value[1:-1].split(",") if item.strip()]
        meta[key.strip()] = value
    if meta.get("name") != path.stem or not meta.get("description"):
        raise ValueError(f"role needs name matching its file and a description: {path}")
    meta.setdefault("skills", [])
    meta["body"] = match.group(2).strip() + "\n"
    return meta


def toml_string(value):
    return json.dumps(value, ensure_ascii=False)


def codex_role(role, skill_root):
    lines = [f"name = {toml_string(role['name'])}", f"description = {toml_string(role['description'])}"]
    if role.get("codex_model"):
        lines.append(f"model = {toml_string(role['codex_model'])}")
    if role.get("codex_effort"):
        lines.append(f"model_reasoning_effort = {toml_string(role['codex_effort'])}")
    if role.get("readonly") == "true":
        lines.append('sandbox_mode = "read-only"')
    lines.append(f"developer_instructions = {toml_string(role['body'])}")
    for skill in role["skills"]:
        lines += ["", "[[skills.config]]", f"path = {toml_string(str(skill_root / skill / 'SKILL.md'))}", "enabled = true"]
    return "\n".join(lines) + "\n"


def claude_role(role):
    lines = ["---", f"name: {role['name']}", f"description: {toml_string(role['description'])}"]
    if role.get("claude_model"):
        lines.append(f"model: {role['claude_model']}")
    if role.get("readonly") == "true":
        lines.append("disallowedTools: Edit, Write, NotebookEdit")
    if role["skills"]:
        lines.append("skills:")
        lines += [f"  - {skill}" for skill in role["skills"]]
    return "\n".join(lines) + "\n---\n\n" + role["body"]


def destinations(args, agent):
    if args.workspace:
        root = args.workspace.resolve()
        base = root / (".codex" if agent == "codex" else ".claude")
        skills = root / ".agents/skills" if agent == "codex" else base / "skills"
    else:
        home = args.home.resolve()
        if agent == "codex":
            base = Path(args.codex_home or os.environ.get("CODEX_HOME") or home / ".codex").resolve()
            skills = home / ".agents/skills"
        else:
            base = Path(args.claude_home or os.environ.get("CLAUDE_CONFIG_DIR") or home / ".claude").resolve()
            skills = base / "skills"
    return skills, base / "agents"


def check_destination(path):
    for part in (path, *path.parents):
        if part.is_symlink():
            raise ValueError(f"destination contains a symlink: {part}")


def publish(entries, directory):
    """Swap staged entries into directory, remove entries a previous install owned, roll back on failure."""
    check_destination(directory)
    directory.mkdir(parents=True, exist_ok=True)
    record = directory / RECORD
    previous = set(json.loads(record.read_text())) if record.exists() else set()
    with tempfile.TemporaryDirectory(prefix=".workflow-kit-", dir=directory) as temp:
        backup = Path(temp)
        moved = []
        try:
            for name in sorted(previous | set(entries)):
                target = directory / name
                if target.is_symlink():
                    raise ValueError(f"destination is a symlink: {target}")
                if target.exists():
                    target.rename(backup / name)
                    moved.append(name)
                if name in entries:
                    shutil.move(entries[name], target)
        except BaseException:
            for name in sorted(set(entries) | previous):
                target = directory / name
                if (backup / name).exists():
                    if target.is_dir():
                        shutil.rmtree(target)
                    elif target.exists():
                        target.unlink()
                    (backup / name).rename(target)
            raise
    record.write_text(json.dumps(sorted(entries), indent=2) + "\n")


def install(args):
    sources = json.loads(args.sources.read_text())
    if sources.get("version") != 2:
        raise ValueError("unsupported sources.json version")
    kit = args.sources.parent / "kit"
    with tempfile.TemporaryDirectory(prefix="workflow-kit-") as temp:
        stage = Path(temp) / "skills"
        stage.mkdir()
        names = []
        for source in sources["upstream"]:
            names += source["skills"]
            fetch_upstream(source, stage)
        for path in sorted((kit / "skills").iterdir()):
            names.append(path.name)
            shutil.copytree(path, stage / path.name)
        if len(names) != len(set(names)) or not all(NAME.fullmatch(name) for name in names):
            raise ValueError(f"invalid or duplicate skill names: {names}")
        roles = [parse_role(path) for path in sorted((kit / "agents").glob("*.md"))]
        for role in roles:
            missing = set(role["skills"]) - set(names)
            if missing:
                raise ValueError(f"{role['name']} requires unknown skills: {sorted(missing)}")
        for agent in args.agents:
            skill_dir, agent_dir = destinations(args, agent)
            copies = Path(temp) / agent
            shutil.copytree(stage, copies / "skills")
            (copies / "agents").mkdir()
            role_files = {}
            for role in roles:
                filename = role["name"] + (".toml" if agent == "codex" else ".md")
                content = codex_role(role, skill_dir) if agent == "codex" else claude_role(role)
                (copies / "agents" / filename).write_text(content)
                role_files[filename] = copies / "agents" / filename
            publish({name: copies / "skills" / name for name in names}, skill_dir)
            publish(role_files, agent_dir)
            print(f"{agent}: {len(names)} skills -> {skill_dir}, {len(roles)} roles -> {agent_dir}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    scope = parser.add_mutually_exclusive_group(required=True)
    scope.add_argument("--workspace", type=Path, nargs="?", const=Path("."),
                       help="Install at PATH, or the current directory when omitted")
    scope.add_argument("--global", dest="global_install", action="store_true")
    parser.add_argument("--agent", choices=[*AGENTS, "all"], default="all")
    parser.add_argument("--home", type=Path, default=Path.home())
    parser.add_argument("--codex-home", type=Path, help="Default: CODEX_HOME or HOME/.codex")
    parser.add_argument("--claude-home", type=Path, help="Default: CLAUDE_CONFIG_DIR or HOME/.claude")
    parser.add_argument("--sources", type=Path, default=ROOT / "sources.json")
    args = parser.parse_args()
    args.agents = AGENTS if args.agent == "all" else (args.agent,)
    try:
        install(args)
    except (OSError, ValueError, KeyError, TypeError, tarfile.TarError) as error:
        print(f"Install failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
