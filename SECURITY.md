# Security Policy

## Security Announcements

- Subscribe to [kubernetes-security-announce] for ecosystem-wide advisories that might also affect this fork.
- Watch the [releases page](https://github.com/redevops-io/ingress-nginx/releases) for redevops.io patch notifications.
- Follow the `#redevops-ingress` channel on the Kubernetes Slack for real-time maintenance updates.

## Reporting a Vulnerability

We strongly prefer coordinated disclosure. Choose whichever option is most convenient:

1. Use GitHub's [private vulnerability reporting](https://github.com/redevops-io/ingress-nginx/security/advisories/new)
	feature. Reports opened there are visible only to the maintainer team.
2. Email `support@redevops.io` with the details. Encrypting the report with the maintainer PGP key (available in the
	repository's Security tab) is appreciated but not required.

Please include:

- A description of the issue and the ingress-nginx versions affected
- Reproduction steps or proof-of-concept
- The Kubernetes version(s) and cloud/distribution you tested on

We aim to acknowledge new reports within **two business days** and provide a remediation plan within **seven days**. If
the issue also affects the upstream Kubernetes project we will coordinate disclosure with the SIG-Network/SIG-Security
maintainers.

## Supported Versions

The redevops.io fork supports the active patch release for each maintained minor listed in the README's compatibility
table. At any point in time this corresponds to the three most recent Kubernetes minors (`n`, `n-1`, `n-2`). Older
branches may receive best-effort fixes for critical CVEs but are not covered by SLA.

For broader Kubernetes version policies, consult the
[Kubernetes version and version skew support policy].

[kubernetes-security-announce]: https://groups.google.com/forum/#!forum/kubernetes-security-announce
[Kubernetes version and version skew support policy]: https://kubernetes.io/docs/setup/release/version-skew-policy/#supported-versions
