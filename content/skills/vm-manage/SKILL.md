---
name: vm-manage
description: Inspect VM inventory or manage VM lifecycle, clones, snapshots, and migrations with explicit scope and approvals.
---

# Inspect or manage VMs

Read the project root's `AGENTS.md` and establish authorized context and namespace
scope before connecting. Discover available MCP tools and schemas; use CLI when
requested or when it is the authorized method. Do not assume workflow names are
real MCP tool names.

For inventory, return available namespace, name, status, CPU, memory, node, and age,
with grouped counts and missing-field limitations. Inventory and snapshot listing
are read-only; do not turn inspection into a mutation.

For create, clone, start, stop, restart, snapshot creation, or migration, inspect
current state, describe affected resources, and obtain approval before acting.
Deletion, snapshot deletion, and restore require the exact affected VM name and
identification of snapshots/data. Read labels and never delete a protected VM.

Return actual resulting state or the observed error. Do not change RBAC, switch
clusters, edit cookbook content, or publish messages to work around a failure.
