# Status

| Item | Value |
|---|---|
| Maturity | Unsupported detached copy of an archived upstream; not independently validated |
| Version | `TAG` file says `v1.14.0` (inherited from upstream). No releases are published from this repository |
| Last git activity | 2026-09-25 (`git log -1 --format=%cs`; clone may be shallow) |
| Upstream | kubernetes/ingress-nginx (archived); closest release `controller-v1.14.0`. See [PROVENANCE.md](PROVENANCE.md) |

## What is supported

Nothing is formally supported. Source is available under Apache-2.0 for reading and for building your own images. The existing caveat stands: **do not use in multi-tenant Kubernetes production installations**; the project assumes users who can create Ingress objects are cluster administrators.

## What is not

- No published images or releases (0 releases; no ingress-nginx package in the org's GHCR packages, checked 2026-10-15).
- No CVE list for fixes made in this repository; "security-hardened" is an unsupported claim.
- No verified security-scan results: the `security-scan` workflow is guarded to run only on `kubernetes/ingress-nginx` and shows `skipped` here.
- No verified support channel: the `#redevops-ingress` Slack channel is unverified. Use GitHub Issues. GitHub private vulnerability reporting is **not enabled** on this repository (API reports `enabled: false`), although `SECURITY.md` references it; the `support@redevops.io` address in `SECURITY.md` is unverified (the org metadata lists `redevops@redevops.io`). Contact to be confirmed.

## Known issues

- Inherited README/Changelog/docs content describes upstream, including CVEs from 2022 and upstream badges.
- Whether the CVE regression tests named in early commit titles exist in the tree is unconfirmed.
