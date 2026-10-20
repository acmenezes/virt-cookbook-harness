---
name: validate
description: Run cookbook lint, build, cross-reference, and document checks and report observed results.
---

# Validate the cookbook

Read `AGENTS.md` at the project root. Use the cookbook working-tree root on a
feature branch because the build writes files. Run `make validate`, retain its
exit status, and inspect complete output, including xref warnings.

Report lint, build, xrefs, and document review as passed, failed, warnings, or not
run. After an early failure, do not assume later checks executed. Identify missing
dependencies instead of installing global software automatically.

Fix requested defects when authorized and rerun affected checks. Report unrelated
preexisting failures and limitations. Do not contact the cluster, publish, or claim
that local validation proves live VM behavior.
