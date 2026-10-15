# Provenance

| Item | Value |
|---|---|
| Upstream | [kubernetes/ingress-nginx](https://github.com/kubernetes/ingress-nginx) (archived upstream) |
| GitHub fork | **No.** `fork=false`; repository created 2025-12-02 (detached copy, default branch `master`) |
| Import commit | `0a33899f1` (2025-12-02) "Initial import from kubernetes/ingress-nginx with security hardening" |
| Upstream baseline | **Closest match: upstream tag `controller-v1.14.0`** (commit `ad643baab`, release published 2025-11-04). The `TAG` file is byte-identical to upstream at that tag (`v1.14.0`), as are `LICENSE` and `pkg/apis/ingress/types.go`; `go.mod`, `NGINX_BASE`, `template.go` and `controller.go` differ. Because history is unrelated, GitHub cannot compute an ahead/behind count. **Exact baseline commit: to be confirmed.** |
| Licence | Apache-2.0, retained from upstream (`LICENSE`) |
| Local history | 85 commits on `master` (GitHub commits API, 2026-10-15) |

## Local delta (summarised from commit titles; not a line-level diff against upstream)

- Import commit (300 files): described as "with security hardening". Follow-up commits on the same day: "Disable cross-namespace annotations"; "Add CVE-2025-1097 regression", "Add CVE-2025-24513 unit test", "Add CVE-2025-24514 regression" (commit titles; matching tests were **not located** in the current tree by text search on 2026-10-15); "updated docs to reflect fork status".
- 2025-12-08 to 2025-12-11: "independent fork operation" infrastructure and many CI/workflow/image-build fixes (about 12 commits).
- 2026-02-07: "Harden location and server_name quoting"; "Guard CI/security workflows on forks".
- 29 commits by `dependabot[bot]` (GitHub Actions and Go module bumps) and merges of those PRs.
- Workflow fixes (k8s-compatibility, ci, secret-scan with gitleaks, golangci-lint); Go toolchain bump (#60); gitignore and clean-up of automation debris.
- README rewritten to describe a "security-hardened fork" (corrected by this notice).

## Caveats

- No CVE list for this repository exists. `Changelog.md` lists CVEs (for example CVE-2022-32149, CVE-2022-27664, CVE-2022-1996 under 1.5.1) that were fixed upstream in 2022; they are inherited, not fixes made here.
- The `security-scan` workflow is guarded by `github.repository == 'kubernetes/ingress-nginx'`, so scheduled/push runs in this repository were observed as `skipped` (for example 2026-10-12 to 2026-10-15). It therefore provides no scan results here.
- 0 GitHub releases; no `ingress-nginx` container package in the organisation's GHCR packages (10 packages listed, none named ingress-nginx), as checked 2026-10-15.
- Badges (CII Best Practices project 5691, Go Report Card) refer to upstream or are unverified for this repository.
