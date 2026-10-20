---
name: review
description: Review a cookbook AsciiDoc file or GitHub pull request and return local findings without editing or posting.
---

# Review content

Read the project root's `AGENTS.md`. Determine whether the input is a local file
or PR. Validate local paths and preserve the user's checkout.

For a file, run `python3 scripts/review-docs.py <file>`. Inspect relevant navigation,
source blocks, terminology, images, and references. Apply the page's module format
rather than requiring tutorial sections on every AsciiDoc file.

For a PR, use `gh pr view` and `gh pr diff`. Check the PR description against its
template, navigation, manifests, and full commit messages, including bodies. Do
not check out the PR over the user's work. Builds write artifacts: run them only
in an authorized disposable checkout or mark build verification not run.

Group findings into errors, warnings, and information, preserving script severity.
Include file/line evidence, suggested fixes, counts, limitations, and a Ready or
Needs revision verdict. Do not edit, commit, contact the cluster, or post reviews
or comments unless explicitly requested.
