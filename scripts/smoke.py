#!/usr/bin/env python3
"""Inspect actual Codex skill discovery without making a model request."""

import argparse
import json
import os
from pathlib import Path
import platform
import queue
import subprocess
import sys
import tempfile
import threading


def discovered_skills(codex, workspace, env):
    process = subprocess.Popen([codex, "app-server", "--stdio"], env=env, stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    messages = queue.Queue()

    def read_output():
        for line in process.stdout:
            messages.put(line)

    threading.Thread(target=read_output, daemon=True).start()

    def request(identifier, method, params):
        process.stdin.write(json.dumps({"id": identifier, "method": method, "params": params}) + "\n")
        process.stdin.flush()
        while True:
            response = json.loads(messages.get(timeout=30))
            if response.get("id") == identifier:
                if "error" in response:
                    raise RuntimeError(response["error"])
                return response["result"]

    try:
        request(1, "initialize", {"clientInfo": {"name": "workflow-smoke", "version": "1"}})
        process.stdin.write(json.dumps({"method": "initialized", "params": {}}) + "\n")
        process.stdin.flush()
        result = request(2, "skills/list", {"cwds": [str(workspace)], "forceReload": True})
        return {skill["name"] for group in result["data"] for skill in group["skills"]
                if Path(skill["path"]).is_relative_to(workspace / ".agents/skills") and skill.get("enabled", True)}
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex", default=os.environ.get("CODEX_BIN", "codex"))
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    manifest = json.loads((root / "manifest.json").read_text())
    with tempfile.TemporaryDirectory(prefix="workflow smoke ") as temp:
        workspace = Path(temp) / "workspace"
        subprocess.run([sys.executable, str(root / "scripts/install.py"), "--workspace", str(workspace)], check=True)
        codex_home = Path(temp) / "codex-home"
        codex_home.mkdir()
        env = dict(os.environ, CODEX_HOME=str(codex_home))
        version = subprocess.run([args.codex, "--version"], env=env, capture_output=True, text=True, check=True).stdout.strip()
        result = subprocess.run([args.codex, "-C", str(workspace), "debug", "prompt-input",
                                 "$development-loop FIXTURE-1"], env=env, capture_output=True, text=True, timeout=45, check=True)
        messages = json.loads(result.stdout)
        context = "\n".join(block.get("text", "") for message in messages if message.get("role") != "user"
                            for block in message.get("content", []))
        expected = {entry["name"] for entry in manifest["skills"]}
        discovered = discovered_skills(args.codex, workspace, env)
        missing = sorted(expected - discovered)
        if missing:
            raise RuntimeError(f"Codex did not discover required skills: {missing}")
        if str(workspace / ".agents/skills") not in context or "- development-loop:" not in context:
            raise RuntimeError("Codex did not report the temporary installation root")
        print(json.dumps({"runtime": version, "os": platform.platform(),
                          "discovered_skills": sorted(discovered), "invocation": "$development-loop FIXTURE-1",
                          "role_files": len(manifest["agents"]),
                          "limits": ["Prompt discovery does not verify custom-role selection or model behavior.",
                                     "Personal user skills may also be visible; no isolation guarantee."]}, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, RuntimeError, queue.Empty, subprocess.SubprocessError) as error:
        print(f"Smoke check failed: {error}", file=sys.stderr)
        sys.exit(1)
