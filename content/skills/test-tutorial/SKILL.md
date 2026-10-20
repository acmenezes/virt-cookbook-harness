---
name: test-tutorial
description: Execute one cookbook tutorial in an authorized cluster scope, repair tutorial defects, and report evidence.
---

# Test a tutorial

Read `AGENTS.md` at the project root. Verify a feature branch, authorized context,
namespace scope, and approvals. Use oc, kubectl, and virtctl for executable steps.
Do not enable access or expand scope to make a test pass.

Read the whole tutorial. Separate host commands, guest commands, runnable
manifests, examples, and expected output. Substitute parameters explicitly. Run
each applicable step once in dependency order; do not apply a manifest twice by
treating its apply command as a separate copy of the same action.

Use bounded waits and record resource, namespace, expected/actual state, duration,
and status. Fix documentation defects and rerun affected steps plus the Python
document reviewer. Report infrastructure failures separately, skip blocked
dependent steps, and stop after three independent infrastructure failures.

Maintain a resource ledger. Obtain applicable destructive confirmation and clean
up only resources created by this run. Never delete preexisting or protected VMs.
Report total/passed/failed/skipped steps, fixes, review results, cleanup, and retained
resources. Never turn a skipped or blocked test into a claimed pass.

Do not create branches, commit, or publish. Return changes and evidence to the
caller; the complete issue pipeline owns its local commits.
