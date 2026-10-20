# OCP Virtualization Cookbook

This is an Antora AsciiDoc site for OpenShift Virtualization, built with pnpm.
Published site: https://redhatquickcourses.github.io/ocp-virt-cookbook.
These rules apply to every supported agent tool. Use the relevant installed skill;
the skills describe procedures, while this file owns the common project policy.

## Project layout and module ownership

Pages live in `modules/<module>/pages/`, navigation in `modules/<module>/nav.adoc`,
downloadable files in `attachments/<tutorial>/`, and screenshots in `images/`.

| Module | Scope |
| --- | --- |
| ROOT | Site entry and overview; no tutorials |
| getting-started | Installation, default storage, first VMs, lifecycle basics, virtctl, cloud-init |
| storage | LVM, HostPath, storage classes, persistent disks |
| networking | UDN, localnet, VLAN, SR-IOV, MetalLB, network policies, addressing and ingress |
| vm-configuration | Access, internal DNS, placement, templates, instance types, hotplug, Windows drivers |
| performance | CPU pinning, NUMA, hugepages, QoS, real-time, monitoring |
| vm-lifecycle | Imports, boot sources, golden images, clones, snapshots and restores |
| manifests | Minimal annotated YAML examples; no procedure tutorials |
| api | Field/API reference; no step-by-step tutorials |
| agentic-vm-management | Agent tooling, skills, and MCP workflows |
| appendix | Glossary only |

Read nearby content before choosing a module or creating a page. Preserve module
boundaries and add new pages to their module's navigation.

Routing boundaries:

- Storage covers backends and storage classes; images, DataVolumes, and boot
  sources belong in vm-lifecycle.
- Networking covers secondary and advanced networks beyond the default pod
  network; internal VM DNS belongs in vm-configuration.
- VM configuration covers day-2 changes; initial creation belongs in getting-started,
  while snapshots and cloning belong in vm-lifecycle.
- Performance covers VM tuning; general node-level tuning is outside scope.

## Git and local work

- Run cookbook commands from its Git working-tree root, not the harness repository.
- Keep all agent configuration and runtime output ignored and untracked in the
  cookbook. Never force-add it. Its maintained source is this separate harness.
- Main is read-only. Create a feature branch before edits, commits, or builds that
  write output. Creating a feature branch or its dedicated worktree is allowed.
- Use `tutorial/issue-<number>` for issue work and `<username>/<short-description>`
  otherwise. Do not reset existing branches or carry unfinished edits onto main.
- Make routine local changes and run checks within the authorized task without
  asking for every edit. Preserve other work; do not reset, stash, clean, or
  overwrite it to proceed. Do not install global dependencies automatically.
- The issue pipeline owns local commits. Standalone writing, review, and testing
  do not commit unless requested. Keep subjects short; add no AI attribution or
  automatic `Co-Authored-By` or `Signed-off-by` trailers.
- Pushes, PR creation, merges, and posting comments/reviews require an explicit
  user request. A review request produces a local report by default.

## Authoring

- Tutorials require Prerequisites, numbered Procedure steps, and Summary. Include
  verification and cleanup for created resources. Overview and See Also are optional.
  Reference, manifest-library, navigation, and glossary pages use their own formats.
- Put `= Page Title` first and use `:navtitle:` when useful. Do not skip heading
  levels. Use one action per numbered step and bulleted prerequisites.
- Every source block declares a language. Host-executable commands use
  `[source,bash,role=execute]`; guest commands and expected output do not. Use
  `[source,text]` for plain output and `[source,yaml]` for valid manifests.
- External links use `link:https://example.com[Label,window=_blank]`; use Antora
  xrefs for pages and attachments. Images need descriptive alt text.
- Use OpenShift and Kubernetes capitalization in prose; do not write `k8s`.
  Remove `creationTimestamp: null` from examples and use YAML block style.
- Write in second person with short, concrete sentences. Avoid filler, inflated
  claims, stock AI phrasing, emojis, and decorative icons. Prefer ASCII diagrams.
- Use the requested product version and verify API details in official docs or
  user-configured references. Do not assume tool-specific aliases, model names,
  reference paths, or a fixed context-window limit.

## Checks and side effects

Run `python3 scripts/review-docs.py <file>` after tutorial edits and fix errors
caused by the change. Run `make validate` before declaring content ready. Inspect
exit status and logs: warnings and unresolved xrefs still need reporting. A passed
script does not waive required sections or prove live cluster behavior.

| Command | Purpose / side effects |
| --- | --- |
| `python3 scripts/review-docs.py --all` | Full document review |
| `make review-file FILE=<path>` | Review one AsciiDoc file through the Makefile |
| `make review` | Review changed AsciiDoc against origin/main |
| `make review-all` | Full document review through the Makefile |
| `make lint` | AsciiDoc syntax; requires Asciidoctor |
| `make build` | Antora output; may install missing Node dependencies |
| `make validate` | Lint, build, xrefs, and full document review |
| `make serve` / `make dev` | Local preview / watch; dev creates runtime files |
| `make setup` | Install cookbook Python/Node dependencies; may install pnpm globally |
| `make test-manifests` | YAML lint; invokes setup prerequisites |
| `make test-manifests-dry` | Manifest dry runs and cluster authentication checks |

Builds need a feature branch or authorized disposable checkout. Report missing
tools before global setup. `make pr` pushes; `make branch` fetches/pulls;
`make sync` rebases. Do not treat these as harmless inspection commands.

## Cluster access and VM protection

Before connecting, establish the authorized cluster context and namespace scope
from the user's request or an explicitly confirmed project configuration. Reuse
established scope and authorization; ask when missing or changed. An existing
login or reachable MCP endpoint alone is not authorization.
Use explicit context/namespace flags where supported. Verify a remote MCP server's
actual cluster separately; the local CLI context does not select its cluster.

- Inventory and snapshot listing are read-only within the authorized scope.
- Describe mutations and obtain explicit approval. A user can authorize a scoped
  tutorial test run in advance, covering creation and modification of its own test
  resources. That does not authorize changing preexisting or cluster-wide resources.
- VM deletion, snapshot deletion, and restore require the exact affected VM name;
  identify snapshots and affected data as well. Test scope alone does not waive
  destructive-operation confirmation.
- Never delete a VM labeled `protected: "true"`, regardless of confirmation.
- Keep a ledger and clean up only test-created resources with the applicable
  authorization. Report retained resources and incomplete cleanup.
- Discover actual MCP tools for VM management; workflow names are not necessarily
  tool names. Do not change RBAC, switch clusters, or bypass tools to work around
  an authorization failure.

Follow dependencies and distinguish tutorial defects from infrastructure failures.
Never claim a live pass for an unexecuted step. Instructions do not replace client
permissions, sandbox controls, or cluster RBAC.
