#!/usr/bin/env python3
"""Copy static cookbook instructions and skills into an ignored Git working tree."""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
TOOLS = ("codex", "claude", "opencode", "cursor")


def git(project, *arguments):
    """Run a Git command in the project and return its output."""
    result = subprocess.run(
        ["git", "-C", str(project), *arguments],
        capture_output=True, text=True, check=False,
    )
    if result.returncode:
        raise ValueError(result.stderr.strip() or "Git command failed")
    return result.stdout


def files_for(tool):
    """Map existing source files to native discovery paths. No rendering."""
    files = [(CONTENT / "AGENTS.md", Path("AGENTS.md"))]
    destination = ".claude/skills" if tool == "claude" else ".agents/skills"
    skills = sorted((CONTENT / "skills").glob("*/SKILL.md"))
    if not skills:
        raise ValueError("No skills found in content/skills")
    for source in skills:
        files.append((source, Path(destination) / source.parent.name / "SKILL.md"))
    if tool == "claude":
        files.append((CONTENT / "claude/CLAUDE.md", Path("CLAUDE.md")))
    elif tool == "cursor":
        files.append((CONTENT / "cursor/cookbook.mdc", Path(".cursor/rules/cookbook.mdc")))
    return files


def check_destination(project, relative):
    """Do not follow old installation links or write into nested repositories."""
    current = project
    for part in relative.parts:
        if current != project and (current / ".git").exists():
            raise ValueError(f"Nested Git repository: {current}; move it aside first")
        current = current / part
        if current.is_symlink():
            raise ValueError(f"Symlink at {current}; remove or migrate it first")
        if current.exists() and current != project / relative and not current.is_dir():
            raise ValueError(f"Parent is not a directory: {current}")
    if current.exists() and not current.is_file():
        raise ValueError(f"Destination is not a regular file: {current}")


def install(project, tool, *, dry_run=False, overwrite=False):
    """Validate and copy the selected tool files into a Git project."""
    project = Path(project).expanduser().resolve(strict=True)
    if not project.is_dir():
        raise ValueError("Project must be a directory")
    if Path(git(project, "rev-parse", "--show-toplevel").strip()).resolve() != project:
        raise ValueError("Pass the project Git working-tree root")
    if project == ROOT or project in ROOT.parents or ROOT in project.parents:
        raise ValueError("The harness and target project must be separate repositories")
    files = files_for(tool)
    roots = {relative.parts[0].casefold() for _, relative in files}
    tracked = git(project, "ls-files", "-z").split("\0")
    if any(name and name.split("/")[0].casefold() in roots for name in tracked):
        raise ValueError("Selected configuration paths are already tracked; the installer will not untrack them")

    # Validate every destination before copying the first file.
    plan = []
    errors = []
    for source, relative in files:
        try:
            if source.is_symlink() or not source.is_file():
                raise ValueError(f"Missing or symlinked source: {source}")
            check_destination(project, relative)
            ignored = subprocess.run(
                ["git", "-C", str(project), "check-ignore", "-q", "--", relative.as_posix()],
                capture_output=True, check=False,
            )
            if ignored.returncode == 1:
                raise ValueError(f"Not ignored: {relative}; add exclusions to .git/info/exclude first")
            if ignored.returncode:
                raise ValueError(f"Git could not check exclusions for {relative}")
            destination = project / relative
            if destination.exists() and destination.read_bytes() == source.read_bytes():
                action = "skip"
            elif destination.exists():
                if not overwrite:
                    raise ValueError(f"Different existing file: {relative}; review it or use --overwrite")
                action = "overwrite"
            else:
                action = "install"
            plan.append((source, relative, action))
        except (OSError, ValueError) as error:
            errors.append(str(error))
    if errors:
        raise ValueError("\n".join(errors))

    for source, relative, action in plan:
        label = f"would {action}" if dry_run and action != "skip" else action
        print(f"{label}: {relative.as_posix()}")
        if not dry_run and action != "skip":
            destination = project / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)


def main():
    """Parse command-line options and run the installer."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, type=Path)
    parser.add_argument("--tool", required=True, choices=TOOLS)
    parser.add_argument("--dry-run", action="store_true", help="Check and list actions without writing")
    parser.add_argument("--overwrite", action="store_true", help="Replace different regular files; no automatic backup")
    args = parser.parse_args()
    try:
        install(args.project, args.tool, dry_run=args.dry_run, overwrite=args.overwrite)
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
