# Contributing Guidelines

Read the following guide if you're interested in contributing to this fork of ingress-nginx. The upstream content (for
example [Make Ingress-Nginx Work for you, and the Community](https://youtu.be/GDm-7BlmPPg)) is still relevant, but the
governance links below describe how redevops.io maintains this repository today.

Note that this guide refers to contributing to actual sources of the repository. If you interested in contributing through issue triaging, have a look at [this guide](./ISSUE_TRIAGE.md).

## Contributor License Agreements

We'd love to accept your patches! Before we can take them, we have to jump a couple of legal hurdles.

Please fill out either the individual or corporate Contributor License Agreement (CLA).

  * Individual contributors retain copyright to their work and contribute under the Developer Certificate of Origin.
    Every commit must include a `Signed-off-by` trailer that states the patch complies with the
    [DCO 1.1](https://developercertificate.org/).
  * If your employer requires a corporate agreement, please contact `legal@redevops.io` so we can countersign a rider.

***NOTE***: We cannot accept code copied from sources that are incompatible with the Apache 2.0 license or whose authors
have not provided a DCO sign-off.

## Finding Issues That Need Help

If you're new to the project and want to help, but don't know where to start, we maintain a semi-curated list of issues
that should not need deep knowledge of the system. [Browse the `good first issue`
label](https://github.com/redevops-io/ingress-nginx/issues?q=is%3Aopen+is%3Aissue+label%3A%22good+first+issue%22).

Alternatively, search for the label [`triage-accepted`](https://github.com/redevops-io/ingress-nginx/issues?q=is%3Aopen+is%3Aissue+label%3Atriage%2Faccepted+) if you have some experience with ingress-nginx. Prioritize issues tagged as
`priority/critical` or security-related when possible.

## Contributing a Patch

1. If you haven't already done so, sign a Contributor License Agreement (see details above).
1. Read the [Ingress development guide](docs/developer-guide/getting-started.md) and the SECURITY.md file.
1. Fork the desired repo, develop and test your code changes.
1. Submit a pull request targeting `master`.

CI runs formatting, unit tests, and the short e2e suites automatically. Please run `gofmt`, `golangci-lint`, and the
relevant `go test ./...` or `make test` targets locally before sending a PR.

All changes must be code reviewed. Coding conventions and standards are explained in the official [developer docs](https://github.com/kubernetes/community/tree/master/contributors/devel). Expect reviewers to request that you avoid common [go style mistakes](https://github.com/golang/go/wiki/CodeReviewComments) in your PRs.

### Merge Approval

Collaborators may add a "LGTM" comment to indicate that a PR is acceptable. Any change requires at least one LGTM from a
reviewer and a final approval from a maintainer in the `OWNERS` file. We do not run Prow in this fork; approvals are
managed directly in GitHub.

Reviewers or members who want to become reviewers should actively search for
[pull requests that need a review](https://github.com/redevops-io/ingress-nginx/pulls?q=is%3Aopen+is%3Apr+label%3Atriage%2Faccepted) and participate in discussions on the linked GitHub Discussions threads.

## Support Channels

Whether you are a user or contributor, official support channels include:

- GitHub issues: https://github.com/redevops-io/ingress-nginx/issues/new/choose
- Slack: `#redevops-ingress` in the [Kubernetes Slack](http://slack.kubernetes.io/)
- Discussions: https://github.com/redevops-io/ingress-nginx/discussions

Before opening a new issue or submitting a new pull request, search the project—it is likely that another user has
already reported the issue you're facing, or it is a known gap that we are already tracking.

## New Contributor Tips
If you're a new contributor, you can follow the [New Contributor Tips guide](NEW_CONTRIBUTOR.md)
