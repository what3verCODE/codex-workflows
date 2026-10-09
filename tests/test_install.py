import io
import json
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = b"---\nname: upstream\ndescription: Fixture.\n---\nUpstream content\n"


def make_archive(path, files):
    with tarfile.open(path, "w:gz") as tar:
        for name, data in files.items():
            info = tarfile.TarInfo("repo-rev/" + name)
            info.size = len(data)
            tar.addfile(info, io.BytesIO(data))


def make_kit(root):
    """A kit source with one upstream skill, one local skill and one read-only role."""
    archive = root / "upstream.tar.gz"
    make_archive(archive, {"skills/upstream/SKILL.md": UPSTREAM, "skills/upstream/ref.md": b"Reference\n",
                           "skills/other/SKILL.md": b"Not requested\n"})
    kit = root / "kit-source"
    (kit / "kit/skills/local").mkdir(parents=True)
    (kit / "kit/skills/local/SKILL.md").write_text("---\nname: local\ndescription: Fixture.\n---\nVersion one\n")
    (kit / "kit/agents").mkdir()
    (kit / "kit/agents/scout.md").write_text(
        "---\nname: scout\ndescription: Find files.\nreadonly: true\nskills: [local, upstream]\n---\n\nRead the task.\n")
    sources = {"version": 2, "upstream": [{"repository": "https://github.com/example/skills", "revision": "abc",
                                           "archive": archive.as_uri(), "skills": {"upstream": "skills/upstream"}}]}
    (kit / "sources.json").write_text(json.dumps(sources))
    return kit, archive


def install(kit, *args):
    command = [sys.executable, str(ROOT / "scripts/install.py"), "--sources", str(kit / "sources.json"), *args]
    return subprocess.run(command, capture_output=True, text=True)


class InstallTests(unittest.TestCase):
    def test_workspace_install_for_both_agents(self):
        with tempfile.TemporaryDirectory(prefix="workflow install ") as tmp:
            kit, _ = make_kit(Path(tmp))
            dest = Path(tmp) / "workspace with spaces"
            result = install(kit, "--workspace", str(dest))
            self.assertEqual(result.returncode, 0, result.stderr)
            for skills in (dest / ".agents/skills", dest / ".claude/skills"):
                self.assertEqual((skills / "upstream/SKILL.md").read_bytes(), UPSTREAM)
                self.assertEqual((skills / "upstream/ref.md").read_text(), "Reference\n")
                self.assertFalse((skills / "other").exists())
                self.assertIn("Version one", (skills / "local/SKILL.md").read_text())
            role = tomllib.loads((dest / ".codex/agents/scout.toml").read_text())
            self.assertEqual(role["sandbox_mode"], "read-only")
            self.assertIn("Read the task.", role["developer_instructions"])
            self.assertEqual([entry["path"] for entry in role["skills"]["config"]],
                             [str(dest / ".agents/skills" / name / "SKILL.md") for name in ("local", "upstream")])
            claude = (dest / ".claude/agents/scout.md").read_text()
            self.assertIn("disallowedTools: Edit, Write, NotebookEdit", claude)
            self.assertIn("  - upstream", claude)
            self.assertFalse((dest / ".git").exists())

    def test_reinstall_replaces_owned_entries_removes_dropped_ones_and_keeps_personal(self):
        with tempfile.TemporaryDirectory() as tmp:
            kit, _ = make_kit(Path(tmp))
            home = Path(tmp) / "home"
            personal = home / ".agents/skills/personal/SKILL.md"
            personal.parent.mkdir(parents=True)
            personal.write_text("Personal")
            args = ("--global", "--agent", "codex", "--home", str(home), "--codex-home", str(home / ".codex"))
            self.assertEqual(install(kit, *args).returncode, 0)
            installed = home / ".agents/skills/local"
            (installed / "stale.md").write_text("Stale")
            (kit / "kit/skills/local/SKILL.md").write_text("---\nname: local\ndescription: Fixture.\n---\nVersion two\n")
            self.assertEqual(install(kit, *args).returncode, 0)
            self.assertIn("Version two", (installed / "SKILL.md").read_text())
            self.assertFalse((installed / "stale.md").exists())
            (kit / "kit/agents/scout.md").unlink()
            (kit / "kit/skills/local/SKILL.md").unlink()
            (kit / "kit/skills/local").rmdir()
            result = install(kit, *args)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(installed.exists())
            self.assertFalse((home / ".codex/agents/scout.toml").exists())
            self.assertTrue((home / ".agents/skills/upstream/SKILL.md").exists())
            self.assertEqual(personal.read_text(), "Personal")
            self.assertFalse((home / ".claude").exists())

    def test_failed_download_leaves_installation_unchanged(self):
        with tempfile.TemporaryDirectory() as tmp:
            kit, archive = make_kit(Path(tmp))
            dest = Path(tmp) / "dest"
            self.assertEqual(install(kit, "--workspace", str(dest)).returncode, 0)
            archive.unlink()
            result = install(kit, "--workspace", str(dest))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("download failed", result.stderr)
            self.assertEqual((dest / ".agents/skills/upstream/SKILL.md").read_bytes(), UPSTREAM)

    def test_symlink_destination_and_unknown_role_skill_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            kit, _ = make_kit(Path(tmp))
            outside = Path(tmp) / "outside"
            outside.mkdir()
            (outside / "SKILL.md").write_text("Keep")
            dest = Path(tmp) / "dest"
            (dest / ".agents/skills").mkdir(parents=True)
            (dest / ".agents/skills/local").symlink_to(outside, target_is_directory=True)
            result = install(kit, "--workspace", str(dest), "--agent", "codex")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("symlink", result.stderr)
            self.assertEqual((outside / "SKILL.md").read_text(), "Keep")
            (kit / "kit/agents/scout.md").write_text("---\nname: scout\ndescription: X.\nskills: [missing]\n---\nBody\n")
            result = install(kit, "--workspace", str(Path(tmp) / "other"))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("missing", result.stderr)

    def test_make_install_reports_missing_prerequisite(self):
        result = subprocess.run(["make", "install", "PYTHON=missing-workflow-python"], cwd=ROOT,
                                capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("requires Python 3.11", result.stderr)


if __name__ == "__main__":
    unittest.main()
