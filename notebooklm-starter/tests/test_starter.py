"""Offline acceptance tests for the self-contained public NotebookLM starter."""
from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import re
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP = ROOT / "scripts" / "bootstrap.py"
REFRESH = ROOT / "scripts" / "refresh.py"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class SetupContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bootstrap = load(BOOTSTRAP, "bootstrap")
        import sys
        sys.modules["bootstrap"] = cls.bootstrap
        cls.refresh = load(REFRESH, "refresh")

    def test_browser_install_avoids_unused_headless_shell(self):
        source = BOOTSTRAP.read_text(encoding="utf-8")
        self.assertIn('"chromium", "--no-shell"', source)

    def test_profile_names_are_explicit_and_path_safe(self):
        good = ("personal", "work", "p", "v", "school_2")
        for value in good:
            self.assertEqual(self.bootstrap.valid_profile(value), value)
        for value in ("", ".", "..", "../other", "hi/there", "hi\\there", "two words", "a"*33, "-wrong", "name@example.com"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.bootstrap.valid_profile(value)

    def test_venv_cli_path_stays_inside_starter(self):
        project = Path("/safe/starter")
        expected_folder = "Scripts" if os.name == "nt" else "bin"
        self.assertEqual(
            self.bootstrap.venv_cli(project),
            project / ".venv" / expected_folder / ("notebooklm.exe" if os.name == "nt" else "notebooklm"),
        )

    def test_explicit_profile_is_used_for_read_only_check(self):
        cmd = self.bootstrap.cli_command(Path("/safe/starter"), "work", "auth", "check", "--test", "--passive")
        self.assertEqual(cmd[1:], ["-p", "work", "auth", "check", "--test", "--passive"])
        self.assertNotIn("--fresh", cmd)

    def test_env_auth_json_removed_without_changing_other_settings(self):
        env = self.bootstrap.cli_env({"NOTEBOOKLM_AUTH_JSON": "sensitive", "NOTEBOOKLM_HOME": "intentional", "OTHER": "yes"})
        self.assertNotIn("NOTEBOOKLM_AUTH_JSON", env)
        self.assertEqual(env["NOTEBOOKLM_HOME"], "intentional")
        self.assertEqual(env["OTHER"], "yes")

    def test_check_never_leaks_cli_output(self):
        b = self.bootstrap
        fake = mock.Mock(returncode=1, stdout="SECRET COOKIE HERE", stderr="SECRET COOKIE HERE")
        with mock.patch.object(b, "venv_cli", return_value=Path("/fake/notebooklm")), mock.patch.object(
            b.subprocess, "run", return_value=fake
        ) as run, mock.patch("builtins.print") as display:
            result = b.check_auth(ROOT, "personal")
            self.assertFalse(result)
            args, kwargs = run.call_args
            self.assertEqual(args[0][-4:], ["auth", "check", "--test", "--passive"])
            self.assertTrue(kwargs["capture_output"])
            self.assertTrue(kwargs["text"])
            printed = " ".join(str(v) for call in display.call_args_list for v in call.args)
            self.assertNotIn("SECRET", printed)

    def test_refresh_refuses_uninitialized_profile(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)
            with mock.patch.object(self.refresh, "auth_storage", return_value=path / "missing.json"), mock.patch.object(
                self.refresh, "venv_cli", return_value=path / "notebooklm"
            ), mock.patch.object(self.refresh.subprocess, "run") as run:
                self.assertFalse(self.refresh.refresh(ROOT, "personal"))
                run.assert_not_called()

    def test_refresh_uses_verified_noninteractive_profile_command(self):
        with tempfile.TemporaryDirectory() as temp:
            storage = Path(temp) / "storage_state.json"
            storage.write_text("fake, not real auth", encoding="utf-8")
            stub_cli = Path(temp) / "notebooklm"
            stub_cli.write_text("mock executable", encoding="utf-8")
            fake = mock.Mock(returncode=0, stdout="", stderr="")
            with mock.patch.object(self.refresh, "auth_storage", return_value=storage), mock.patch.object(
                self.refresh, "venv_cli", return_value=stub_cli
            ), mock.patch.object(self.refresh.subprocess, "run", return_value=fake) as run:
                self.assertTrue(self.refresh.refresh(ROOT, "work"))
                cmd = run.call_args.args[0]
                self.assertEqual(cmd[1:], ["-p", "work", "auth", "refresh", "--verify", "--quiet"])
                self.assertTrue(run.call_args.kwargs["capture_output"])
                self.assertNotIn("NOTEBOOKLM_AUTH_JSON", run.call_args.kwargs["env"])

    def test_public_tree_is_self_contained_and_has_no_private_session_files(self):
        required = (
            "README.md", "SKILL.md", "requirements.txt", ".gitignore",
            "references/WORKFLOWS.md", "references/SECURITY.md",
            "scripts/bootstrap.py", "scripts/refresh.py",
            "scripts/register_keepalive.ps1",
        )
        for name in required:
            with self.subTest(path=name):
                self.assertTrue((ROOT / name).is_file())
        for path in ROOT.rglob("*"):
            # Installed dependencies are intentionally gitignored and never published.
            if ".venv" in path.parts or "__pycache__" in path.parts:
                continue
            if path.is_file():
                self.assertNotIn(path.name, ("storage_state.json", "master_token.json", "context.json"))
                self.assertNotIn(".venv", path.parts)
                if path.suffix.lower() in (".md", ".py", ".ps1", ".txt"):
                    text = path.read_text(encoding="utf-8")
                    self.assertNotRegex(text, r"(?i)C:[/\\]Users[/\\][^/\\]+")
                    self.assertNotRegex(text, r"(?i)[a-z0-9._%+-]+@(?:gmail|googlemail)\.com")
                    self.assertNotIn("NOTEBOOKLM_AUTH_JSON" + "=", text)

    def test_agent_guide_requires_owner_approval_and_identity(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8").lower()
        for phrase in ("approval", "profile", "account", "login", "security", "read-only", "no passwords"):
            self.assertIn(phrase, skill)
        self.assertIn("notebooklm-py[browser]==0.8.6", (ROOT / "requirements.txt").read_text(encoding="utf-8"))

if __name__ == "__main__":
    unittest.main()
