#!/usr/bin/env python3
"""Pin every upstream source in sources.json to its repository's latest default-branch commit."""

import json
from pathlib import Path
import subprocess


def main():
    path = Path(__file__).resolve().parents[1] / "sources.json"
    sources = json.loads(path.read_text())
    for source in sources["upstream"]:
        head = subprocess.run(["git", "ls-remote", source["repository"], "HEAD"],
                              capture_output=True, text=True, check=True).stdout.split()[0]
        if head != source["revision"]:
            print(f"{source['repository']}: {source['revision'][:10]} -> {head[:10]}")
            source["revision"] = head
    path.write_text(json.dumps(sources, indent=2) + "\n")


if __name__ == "__main__":
    main()
