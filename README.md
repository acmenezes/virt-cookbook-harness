# virt-cookbook-harness

Project-specific AI instructions and workflow skills for contributors to the
[OpenShift Virtualization Cookbook](https://github.com/RedHatQuickCourses/ocp-virt-cookbook).
The cookbook contains practical tutorials for deploying and managing virtual
machines on OpenShift Virtualization. This repository supplies the context and
workflows AI coding tools need to work on that cookbook consistently.

The harness is maintained separately from the cookbook. Its installer copies
the selected configuration into the cookbook checkout so the files are available
to an AI tool without adding harness configuration to cookbook commits.

## What’s included

- `content/AGENTS.md` provides shared cookbook context, authoring conventions,
  repository guidance, and safeguards for cluster and VM operations.
- `content/skills/` provides five focused workflows:
  - `new-tutorial` writes or improves tutorials and can process supplied issues.
  - `review` reviews a local page or pull request and returns local findings.
  - `test-tutorial` tests a tutorial against an authorized cluster scope.
  - `validate` runs the cookbook’s lint, build, cross-reference, and document checks.
  - `vm-manage` inspects or manages VMs within the authorized scope.
- `content/claude/CLAUDE.md` and `content/cursor/cookbook.mdc` are tool-specific
  entry points that refer back to the shared instructions.
- `install.py` copies the instructions and skills into the discovery paths for
  the selected tool.

## Install into the cookbook

You need Python 3.11 or newer and Git. Check out both repositories locally, then
add these entries to the cookbook repository’s `.git/info/exclude` file:

```gitignore
/AGENTS.md
/CLAUDE.md
/.agents/
/.claude/
/.cursor/
```

These local exclusions keep AI configuration out of cookbook commits. The
installer does not modify the exclude file. From this repository, preview and
then install the configuration into the root of your cookbook checkout:

```console
python3 install.py --project /path/to/ocp-virt-cookbook --tool codex --dry-run
python3 install.py --project /path/to/ocp-virt-cookbook --tool codex
```

Choose the client you use with `--tool`:

| Tool | Installed files in the cookbook checkout |
| --- | --- |
| Codex | `AGENTS.md`, `.agents/skills/` |
| OpenCode | `AGENTS.md`, `.agents/skills/` |
| Claude Code | `AGENTS.md`, `CLAUDE.md`, `.claude/skills/` |
| Cursor | `AGENTS.md`, `.agents/skills/`, `.cursor/rules/cookbook.mdc` |

Run the installer once for each client you use. Codex and OpenCode share the
same skill paths, and identical files are skipped on repeat installs.

The installer requires the target to be the root of a separate Git working tree.
It checks all destinations before copying and refuses tracked or non-ignored
configuration, symlinks, nested repositories, and different existing files.
Use `--dry-run` to inspect actions. If you have reviewed existing configuration
and want to replace differing files, pass `--overwrite`; it does not create
backups.

## Use the workflows

Open the cookbook checkout in your AI coding tool. The tool reads the installed
project instructions, and you can ask for a task such as writing a tutorial,
reviewing a page, or validating documentation. The agent should follow the
corresponding skill in `.agents/skills/` or `.claude/skills/`.

The skills follow the cookbook’s local workflow. For example, content changes
belong on a feature branch, and validation runs from the cookbook repository.
Live tutorial tests and VM operations require an explicitly authorized cluster
context and namespace. The instructions do not grant cluster access or replace
the permissions of your client or cluster account.

## Maintain the harness

Edit the maintained source files under `content/`, review the changes, and
rerun the installer for the relevant client. Do not edit the installed copies as
the source of truth; the next install may replace them. The installer copies
files unchanged.

The harness contains configuration and workflow guidance. Cookbook tutorials,
images, manifests, and navigation remain maintained in the
[cookbook repository](https://github.com/RedHatQuickCourses/ocp-virt-cookbook).
