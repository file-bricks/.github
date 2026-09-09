"""Test suite verifying profile parity, repository indexing, and link integrity for file-bricks."""
from pathlib import Path
import re
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

EXPECTED_PUBLIC_REPOS = [
    ".github",
    "AmpelClip",
    "CloudLockFixer",
    "ExplorerPro",
    "LaunchBoards",
    "NoteSpaceLLM",
    "ProFiler",
    "ProSync",
    "ProfiPrompt",
    "RSS-BOOK",
    "RSS-BOOKSTORE",
    "SQLiteViewer",
    "SoftwareCenter",
    "WinStorePackager",
    "knowledgedigest",
    "promptboard",
]


def test_public_repo_count():
    assert len(EXPECTED_PUBLIC_REPOS) == 16


def test_readme_badges():
    profile_en = (REPO_ROOT / "profile" / "README.md").read_text(encoding="utf-8")
    profile_de = (REPO_ROOT / "profile" / "README_de.md").read_text(encoding="utf-8")
    root_readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")

    assert "Public_Repos-16-blue.svg" in profile_en
    assert "Öffentliche_Repos-16-blue.svg" in profile_de
    assert "Public_Repos-16-blue.svg" in root_readme


def test_last_checked_dates():
    profile_en = (REPO_ROOT / "profile" / "README.md").read_text(encoding="utf-8")
    profile_de = (REPO_ROOT / "profile" / "README_de.md").read_text(encoding="utf-8")
    root_readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    llms_txt = (REPO_ROOT / "llms.txt").read_text(encoding="utf-8")

    assert "last-checked: 2026-09-09" in profile_en
    assert "last-checked: 2026-09-09" in profile_de
    assert "2026-09-09" in root_readme
    assert "Last-checked: 2026-09-09" in llms_txt


def test_all_repos_indexed_in_profile_en():
    content = (REPO_ROOT / "profile" / "README.md").read_text(encoding="utf-8")
    for repo in EXPECTED_PUBLIC_REPOS:
        assert repo in content, f"Repo {repo} missing from profile/README.md"


def test_all_repos_indexed_in_profile_de():
    content = (REPO_ROOT / "profile" / "README_de.md").read_text(encoding="utf-8")
    for repo in EXPECTED_PUBLIC_REPOS:
        assert repo in content, f"Repo {repo} missing from profile/README_de.md"


def test_all_repos_indexed_in_root_readme():
    content = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    for repo in EXPECTED_PUBLIC_REPOS:
        assert repo in content, f"Repo {repo} missing from README.md"


def test_all_repos_indexed_in_llms_txt():
    content = (REPO_ROOT / "llms.txt").read_text(encoding="utf-8")
    for repo in EXPECTED_PUBLIC_REPOS:
        assert repo in content, f"Repo {repo} missing from llms.txt"


def test_softwarecenter_banner_presence():
    profile_en = (REPO_ROOT / "profile" / "README.md").read_text(encoding="utf-8")
    profile_de = (REPO_ROOT / "profile" / "README_de.md").read_text(encoding="utf-8")

    banner_url = "https://raw.githubusercontent.com/file-bricks/SoftwareCenter/master/assets/banner.svg"
    assert banner_url in profile_en, "SoftwareCenter banner missing from profile/README.md"
    assert banner_url in profile_de, "SoftwareCenter banner missing from profile/README_de.md"


def test_mermaid_syntax_parentheses_quoted():
    """Mermaid labels containing parentheses must be quoted to prevent parsing errors."""
    for path in [REPO_ROOT / "profile" / "README.md", REPO_ROOT / "profile" / "README_de.md"]:
        content = path.read_text(encoding="utf-8")
        mermaid_blocks = re.findall(r"```mermaid\n(.*?)```", content, re.DOTALL)
        assert len(mermaid_blocks) > 0, f"No mermaid block in {path}"
        for block in mermaid_blocks:
            for line in block.splitlines():
                line = line.strip()
                if "(" in line and ")" in line:
                    # Line with parentheses should have quotes around the node text e.g. ["...(...)"]
                    assert '["' in line and '"]' in line, f"Unquoted parentheses in mermaid line: {line} in {path}"
