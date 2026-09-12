import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class BootstrapTests(unittest.TestCase):
    def test_default_is_global_and_download_failure_does_not_run_installer(self):
        with tempfile.TemporaryDirectory(prefix="bootstrap global ") as tmp:
            root = Path(tmp)
            source = root / "source"
            (source / "scripts").mkdir(parents=True)
            # Stub the destination installer boundary to observe defaults without
            # installing anything into the test runner's actual home.
            (source / "scripts/install.py").write_text("import sys\nprint('DESTINATION_ARGS=' + repr(sys.argv[1:]))\n")
            (source / "manifest.json").write_text("{}")
            archive = root / "kit.tar.gz"
            with tarfile.open(archive, "w:gz") as tar:
                tar.add(source, arcname="kit-revision")
            env = dict(os.environ, CODEX_WORKFLOW_ARCHIVE_URL=archive.as_uri(), PYTHON=sys.executable)
            script = (ROOT / "setup.sh").read_text()
            result = subprocess.run(["sh"], input=script, env=env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("DESTINATION_ARGS=['--global']", result.stdout)
            archive.unlink()
            result = subprocess.run(["sh"], input=script, env=env, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertNotIn("DESTINATION_ARGS=", result.stdout)

    def test_piped_script_installs_archive_and_reinstalls_without_git_or_make(self):
        with tempfile.TemporaryDirectory(prefix="bootstrap test ") as tmp:
            root = Path(tmp)
            source = root / "source"
            (source / "scripts").mkdir(parents=True)
            shutil.copyfile(ROOT / "scripts/install.py", source / "scripts/install.py")
            skill = source / "example"
            skill.mkdir()
            (skill / "SKILL.md").write_text("---\nname: example\ndescription: Fixture.\n---\nAuthoritative\n")
            (source / "manifest.json").write_text(json.dumps({"version": 1, "skills": [
                {"name": "example", "kind": "local", "path": "example"}], "agents": []}))
            archive = root / "kit.tar.gz"
            with tarfile.open(archive, "w:gz") as tar:
                tar.add(source, arcname="kit-revision")
            dest = root / "workspace with spaces"
            env = dict(os.environ, CODEX_WORKFLOW_ARCHIVE_URL=archive.as_uri(), PYTHON=sys.executable)
            command = ["sh", "-s", "--", "--workspace", str(dest)]
            script = (ROOT / "setup.sh").read_text()
            first = subprocess.run(command, input=script, env=env, capture_output=True, text=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            installed = dest / ".agents/skills/example/SKILL.md"
            installed.write_text("Local change")
            personal = dest / ".agents/skills/personal/SKILL.md"
            personal.parent.mkdir()
            personal.write_text("Keep")
            second = subprocess.run(command, input=script, env=env, capture_output=True, text=True)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertIn("Authoritative", installed.read_text())
            self.assertEqual(personal.read_text(), "Keep")
            self.assertFalse((dest / ".git").exists())


if __name__ == "__main__":
    unittest.main()
