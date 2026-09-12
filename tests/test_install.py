import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class InstallTests(unittest.TestCase):
    def test_unsafe_manifest_and_symlink_destination_do_not_touch_other_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "example"
            source.mkdir()
            (source / "SKILL.md").write_text("---\nname: example\ndescription: Fixture.\n---\nNew\n")
            outside = root / "outside"
            outside.mkdir()
            (outside / "SKILL.md").write_text("Keep")
            dest = root / "dest"
            skills = dest / ".agents/skills"
            skills.mkdir(parents=True)
            (skills / "example").symlink_to(outside, target_is_directory=True)
            manifest = root / "manifest.json"
            spec = {"version": 1, "skills": [{"name": "example", "kind": "local", "path": "example"}], "agents": []}
            manifest.write_text(json.dumps(spec))
            command = [sys.executable, str(ROOT / "scripts/install.py"), "--workspace", str(dest), "--manifest", str(manifest)]
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("symlink", result.stderr.lower())
            self.assertEqual((outside / "SKILL.md").read_text(), "Keep")
            spec["skills"][0]["name"] = "../escape"
            manifest.write_text(json.dumps(spec))
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("name", result.stderr.lower())
            self.assertFalse((dest / ".agents/escape").exists())

    def test_make_install_reports_missing_prerequisite(self):
        result = subprocess.run(["make", "install", "PYTHON=missing-workflow-python"], cwd=ROOT,
                                capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("requires Python 3.11", result.stderr)

    def test_pinned_download_and_failed_update_leave_installation_unchanged(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            payload = b"---\nname: upstream\ndescription: Fixture.\n---\nUpstream content\n"
            download = root / "download.md"
            download.write_bytes(payload)
            manifest = root / "manifest.json"
            spec = {"version": 1, "skills": [{"name": "upstream", "kind": "upstream",
                    "files": [{"path": "SKILL.md", "url": download.as_uri(),
                               "sha256": hashlib.sha256(payload).hexdigest()}]}], "agents": []}
            manifest.write_text(json.dumps(spec))
            dest = root / "dest"
            command = [sys.executable, str(ROOT / "scripts/install.py"), "--workspace", str(dest),
                       "--manifest", str(manifest)]
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            installed = dest / ".agents/skills/upstream/SKILL.md"
            self.assertEqual(installed.read_bytes(), payload)
            download.write_bytes(b"tampered")
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("SHA-256", result.stderr)
            self.assertEqual(installed.read_bytes(), payload)
            download.unlink()
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("download", result.stderr.lower())
            self.assertEqual(installed.read_bytes(), payload)

    def test_global_reinstall_replaces_managed_tree_and_preserves_personal_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source"
            skill = source / "example"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("---\nname: example\ndescription: Fixture.\n---\nVersion one\n")
            manifest = source / "manifest.json"
            manifest.write_text(json.dumps({"version": 1, "skills": [
                {"name": "example", "kind": "local", "path": "example"}
            ], "agents": []}))
            home = root / "home"
            codex_home = root / "custom codex home"
            codex_home.mkdir()
            config = codex_home / "config.toml"
            config.write_text('# personal policy\nmodel = "my-model"\n')
            unrelated = home / ".agents/skills/personal/SKILL.md"
            unrelated.parent.mkdir(parents=True)
            unrelated.write_text("Personal")
            command = [sys.executable, str(ROOT / "scripts/install.py"), "--global",
                       "--home", str(home), "--codex-home", str(codex_home),
                       "--manifest", str(manifest)]
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            installed = home / ".agents/skills/example"
            (installed / "stale.md").write_text("Stale")
            (installed / "SKILL.md").write_text("Local modification")
            (skill / "SKILL.md").write_text("---\nname: example\ndescription: Fixture.\n---\nVersion two\n")
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Version two", (installed / "SKILL.md").read_text())
            self.assertFalse((installed / "stale.md").exists())
            self.assertEqual(unrelated.read_text(), "Personal")
            self.assertEqual(config.read_text(), '# personal policy\nmodel = "my-model"\n')
            manifest.write_text(json.dumps({"version": 1, "skills": [], "agents": []}))
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((installed / "SKILL.md").exists())

    def test_workspace_install_without_git_and_with_spaces(self):
        with tempfile.TemporaryDirectory(prefix="workflow install ") as tmp:
            root = Path(tmp)
            source = root / "source"
            skill = source / "skills" / "example"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("---\nname: example\ndescription: Fixture skill.\n---\nRead the task.\n")
            agents = source / "agents"
            agents.mkdir()
            (agents / "scout.toml").write_text('name = "scout"\ndescription = "Find files"\ndeveloper_instructions = "Read the task"\n')
            manifest = source / "manifest.json"
            manifest.write_text(json.dumps({"version": 1, "skills": [
                {"name": "example", "kind": "local", "path": "skills/example"}
            ], "agents": [{"name": "scout", "path": "agents/scout.toml", "skills": ["example"]}]}))
            dest = root / "workspace with spaces"
            result = subprocess.run([sys.executable, str(ROOT / "scripts/install.py"),
                                     "--workspace", str(dest), "--manifest", str(manifest)],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual((dest / ".agents/skills/example/SKILL.md").read_text(),
                             (skill / "SKILL.md").read_text())
            self.assertTrue((dest / ".codex/agents/scout.toml").is_file())
            self.assertFalse((dest / ".git").exists())
            self.assertFalse((dest / ".codex/config.toml").exists())


if __name__ == "__main__":
    unittest.main()
