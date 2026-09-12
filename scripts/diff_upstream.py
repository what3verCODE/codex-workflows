#!/usr/bin/env python3
"""Show all maintained fork differences against their pinned upstream revisions."""

import argparse
import difflib
import json
from pathlib import Path
import sys
import urllib.request


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkout", type=Path, help="Use an existing upstream checkout at the recorded revision")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    manifest = json.loads((root / "manifest.json").read_text())
    for entry in manifest["skills"]:
        if entry["kind"] != "local" or "upstream" not in entry:
            continue
        origin = entry["upstream"]
        repo = origin["repository"].removeprefix("https://github.com/")
        revision = origin["revision"]
        print(f"\n# {entry['name']} against {repo}@{revision}")
        if args.checkout:
            import subprocess
            actual = subprocess.check_output(["git", "-C", str(args.checkout), "rev-parse", "HEAD"], text=True).strip()
            if actual != revision:
                raise ValueError(f"checkout revision {actual} does not match {revision}")
            paths = subprocess.check_output(["git", "-C", str(args.checkout), "ls-tree", "-r", "--name-only",
                                             revision, "--", origin["path"]], text=True).splitlines()
            prefix = origin["path"] + "/"
            originals = {path[len(prefix):]: subprocess.check_output(
                ["git", "-C", str(args.checkout), "show", f"{revision}:{path}"]) for path in paths}
        else:
            request = urllib.request.Request(f"https://api.github.com/repos/{repo}/git/trees/{revision}?recursive=1",
                                             headers={"User-Agent": "codex-workflow-upstream-diff"})
            with urllib.request.urlopen(request, timeout=30) as response:
                tree = json.load(response)
            if tree.get("truncated"):
                raise ValueError("upstream tree is truncated; use UPSTREAM_CHECKOUT at the pinned revision")
            prefix = origin["path"] + "/"
            originals = {}
            for item in tree["tree"]:
                if item["type"] == "blob" and item["path"].startswith(prefix):
                    url = f"https://raw.githubusercontent.com/{repo}/{revision}/{item['path']}"
                    with urllib.request.urlopen(url, timeout=30) as response:
                        originals[item["path"][len(prefix):]] = response.read()
        local = root / entry["path"]
        maintained = {str(p.relative_to(local)): p.read_bytes() for p in local.rglob("*") if p.is_file()
                      and p.name not in ("LICENSE", "upstream.json")}
        for name in sorted(originals.keys() | maintained.keys()):
            before, after = originals.get(name, b""), maintained.get(name, b"")
            if before != after:
                print("".join(difflib.unified_diff(before.decode().splitlines(True), after.decode().splitlines(True),
                                                  fromfile=f"upstream/{entry['name']}/{name}",
                                                  tofile=f"kit/skills/{entry['name']}/{name}")), end="")
        print("License and upstream.json are added attribution metadata.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError) as error:
        print(f"Upstream comparison failed: {error}", file=sys.stderr)
        sys.exit(1)
