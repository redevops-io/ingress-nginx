## Open PR Triage

Generated from `.sidekick/open_prs.json` and `.sidekick/pr_results_mod_*.json`.

| PR | Title | Head SHA | Base Ref | Mergeable | Failing Checks | Rebase Status |
|---|---|---|---|---|---|---|
| #20 | Bump k8s.io/apimachinery from 0.34.2 to 0.35.1 in /images/ext-auth-example-authsvc/rootfs | `a3a1ce3` | master | — | sanity check failed | could not check |
| #21 | Bump google.golang.org/grpc from 1.77.0 to 1.79.1 in /images/go-grpc-greeter-server/rootfs | `50b8bb3` | master | — | — | rebased with conflicts |
| #22 | Bump k8s.io/client-go from 0.34.2 to 0.35.1 in /images/kube-webhook-certgen/rootfs | `ade245d` | master | — | — | could not check |
| #23 | Bump k8s.io/apimachinery from 0.34.2 to 0.35.1 in /images/kube-webhook-certgen/rootfs | `6d5beb3` | master | — | — | could not check |
| #24 | Bump k8s.io/client-go from 0.34.2 to 0.35.1 | `62c63af` | master | — | sanity check failed | could not check |
| #25 | Bump k8s.io/apimachinery from 0.34.2 to 0.35.1 | `6cb48ec` | master | — | — | rebased with conflicts |
| #26 | Bump google.golang.org/grpc from 1.77.0 to 1.79.1 | `73a1f8c` | master | — | — | could not check |
| #28 | chore(deps): bump the actions group with 4 updates | `0c240a0` | master | — | sanity check failed | could not check |
| #29 | chore(deps): bump actions/download-artifact from 4 to 8 | `644fc88` | master | — | — | rebased ok |
| #30 | chore(deps): bump actions/upload-artifact from 6.0.0 to 7.0.1 | `62c63af` | master | — | — | could not check |
| #31 | chore(deps): bump azure/setup-helm from 4.3.1 to 5.0.0 | `d380e1d` | master | — | — | could not check |
| #32 | chore(deps): bump docker/login-action from 3 to 4 | `47bac83` | master | — | sanity check failed | could not check |
| #33 | chore(deps): bump the docker group across 3 directories with 1 update | `70b9f6b` | master | — | — | rebased ok |

## Notes

- **Mergeable**: `null` in source data means GitHub has not yet computed mergeability.
- **Failing Checks**: Based on `statusCheckRollup` (all `null` here) and local sanity-check results from `pr_results_mod_0.json`.
- **Rebase Status**:
  - `rebased ok` — cherry-pick / rebase succeeded with no conflicts.
  - `rebased with conflicts` — rebase could not be completed automatically.
  - `could not check` — no rebase attempt was recorded for this PR.
