from __future__ import annotations

import hashlib
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "skills" / "orchestrate-sol-luna"
SKILL_PATH = SKILL_ROOT / "SKILL.md"
INTERFACE_PATH = SKILL_ROOT / "agents" / "openai.yaml"
PROFILE_PATH = SKILL_ROOT / "assets" / "agents" / "luna-implementer.toml"

EXPECTED_FILES = {
    ".editorconfig",
    ".gitignore",
    ".github/CODEOWNERS",
    ".github/ISSUE_TEMPLATE/bug_report.md",
    ".github/ISSUE_TEMPLATE/config.yml",
    ".github/ISSUE_TEMPLATE/feature_request.md",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/dependabot.yml",
    ".github/workflows/validate.yml",
    "CHANGELOG.md",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "NOTICE.md",
    "README.md",
    "SECURITY.md",
    "VERSION",
    "skills/orchestrate-sol-luna/SKILL.md",
    "skills/orchestrate-sol-luna/agents/openai.yaml",
    "skills/orchestrate-sol-luna/assets/agents/luna-implementer.toml",
    "tests/test_package.py",
}

EXPECTED_SOURCE_HASHES = {
    "skills/orchestrate-sol-luna/SKILL.md": "96e1d9ff82347153c3e2f2fbc6981fa61d4361c28107a1545c3f6b46694e83f2",
    "skills/orchestrate-sol-luna/agents/openai.yaml": "1f135484352e7e293f6bd5a1b98dd1d862d6305e65871004518ca8a688f91b90",
    "skills/orchestrate-sol-luna/assets/agents/luna-implementer.toml": "b35416a1d9d0e3017c0f6ae35faf32935a5a06faf01320fa9f9919b876e667fb",
}

PACKET_LABELS = (
    "Objective",
    "Acceptance criteria",
    "Non-goals",
    "Repository instructions",
    "Current worktree constraints",
    "Relevant files and symbols",
    "Observed behavior and evidence",
    "Implementation sequence",
    "Interfaces and invariants to preserve",
    "Required verification commands",
    "Risks and edge cases",
    "Expected worker report",
)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_frontmatter(path: Path) -> tuple[dict[str, str], str]:
    lines = read_text(path).splitlines()
    if not lines or lines[0] != "---":
        raise AssertionError(f"{path} does not start with YAML frontmatter")
    try:
        end = lines.index("---", 1)
    except ValueError as error:
        raise AssertionError(f"{path} has no frontmatter terminator") from error

    metadata: dict[str, str] = {}
    for line in lines[1:end]:
        key, separator, value = line.partition(":")
        if not separator:
            raise AssertionError(f"unsupported frontmatter line: {line!r}")
        metadata[key.strip()] = value.strip()
    body = "\n".join(lines[end + 1 :])
    return metadata, body


def parse_simple_toml_assignments(path: Path) -> dict[str, str]:
    assignments: dict[str, str] = {}
    for line in read_text(path).splitlines():
        match = re.fullmatch(r'([A-Za-z_][A-Za-z0-9_]*)\s*=\s*"([^"]*)"', line)
        if match:
            assignments[match.group(1)] = match.group(2)
    return assignments


class PackageContractTests(unittest.TestCase):
    def test_skill_frontmatter(self) -> None:
        metadata, _ = parse_frontmatter(SKILL_PATH)
        self.assertEqual(metadata["name"], "orchestrate-sol-luna")
        self.assertIn("GPT-5.6 Sol", metadata["description"])
        self.assertIn("GPT-5.6 Luna", metadata["description"])

    def test_required_packet_label_order(self) -> None:
        _, body = parse_frontmatter(SKILL_PATH)
        positions = []
        for label in PACKET_LABELS:
            match = re.search(rf"(?m)^{re.escape(label)}$", body)
            self.assertIsNotNone(match, f"missing packet label: {label}")
            positions.append(match.start())
        self.assertEqual(positions, sorted(positions))

    def test_packaged_luna_profile(self) -> None:
        profile = parse_simple_toml_assignments(PROFILE_PATH)
        self.assertEqual(profile["name"], "luna_implementer")
        self.assertEqual(profile["model"], "gpt-5.6-luna")
        self.assertEqual(profile["model_reasoning_effort"], "max")

    def test_no_delegation_constraint(self) -> None:
        skill = read_text(SKILL_PATH)
        profile = read_text(PROFILE_PATH)
        self.assertIn("Do not spawn extra supervisors or auxiliary agents", skill)
        self.assertIn("Luna is the only writer", skill)
        self.assertIn("Do not spawn other agents.", profile)
        self.assertIn("Never silently substitute a model or lower effort", skill)

    def test_interface_metadata(self) -> None:
        interface = read_text(INTERFACE_PATH)
        self.assertIn('display_name: "Sol-Luna Orchestrator"', interface)
        self.assertIn('short_description: "Sol plans complex work; Luna implements"', interface)
        self.assertIn("$orchestrate-sol-luna", interface)

    def test_supplied_source_hashes(self) -> None:
        for relative_path, expected_hash in EXPECTED_SOURCE_HASHES.items():
            path = ROOT / relative_path
            actual_hash = hashlib.sha256(path.read_bytes()).hexdigest()
            self.assertEqual(actual_hash, expected_hash, relative_path)

    def test_release_metadata_and_boundaries(self) -> None:
        readme = read_text(ROOT / "README.md")
        changelog = read_text(ROOT / "CHANGELOG.md")
        version = read_text(ROOT / "VERSION").strip()
        self.assertEqual(version, "0.1.0")
        self.assertRegex(changelog, r"(?m)^## \[0\.1\.0\] - 2026-09-06$")
        self.assertIn("current public release is 0.1.0", readme.lower())
        self.assertIn("unofficial community project", readme.lower())
        self.assertIn("environment-dependent", readme.lower())
        self.assertIn("does not grant permissions", readme.lower())
        self.assertIn("silent", readme.lower())
        self.assertRegex(readme, r"does not modify\s+~/.codex/config\.toml")

    def test_package_layout(self) -> None:
        actual_files = {
            path.relative_to(ROOT).as_posix()
            for path in ROOT.rglob("*")
            if path.is_file()
            and ".git" not in path.parts
            and "__pycache__" not in path.parts
        }
        self.assertEqual(actual_files, EXPECTED_FILES)

    def test_ci_is_read_only(self) -> None:
        workflow = read_text(ROOT / ".github/workflows/validate.yml")
        self.assertIn("permissions:\n  contents: read", workflow)
        self.assertIn("actions/checkout@v4", workflow)
        self.assertIn("actions/setup-python@v5", workflow)
        self.assertIn('python-version: "3.12"', workflow)
        self.assertNotIn("contents: write", workflow)
        self.assertNotIn("read-write", workflow)


if __name__ == "__main__":
    unittest.main()
