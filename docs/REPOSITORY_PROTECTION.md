# Repository Protection Guide

This document explains how to protect the redevops-io/ingress-nginx fork from unauthorized modifications.

## Branch Protection Rules

To prevent unauthorized changes to the `master` branch, configure these GitHub settings:

### Navigate to Settings
1. Go to https://github.com/redevops-io/ingress-nginx/settings/branches
2. Click "Add branch protection rule"
3. Set branch name pattern to: `master`

### Required Settings

#### Protect matching branches
- ✅ **Require a pull request before merging**
  - ✅ Require approvals: `1`
  - ✅ Dismiss stale pull request approvals when new commits are pushed
  - ✅ Require review from Code Owners (if CODEOWNERS file exists)

- ✅ **Require status checks to pass before merging**
  - ✅ Require branches to be up to date before merging
  - Select relevant CI checks once they're running (e.g., unit tests, linting)

- ✅ **Require conversation resolution before merging**

- ✅ **Require signed commits** (recommended for security)

- ✅ **Require linear history** (prevents messy merges)

- ✅ **Do not allow bypassing the above settings**
  - Uncheck "Allow administrators to bypass" unless you need emergency access

#### Rules applied to everyone including administrators
- ✅ **Restrict who can push to matching branches**
  - Add only trusted maintainers to the allowlist
  - Leave empty to require PRs from everyone

- ✅ **Allow force pushes**: `Disabled`
- ✅ **Allow deletions**: `Disabled`

### Additional Repository Settings

#### General Settings
Navigate to: https://github.com/redevops-io/ingress-nginx/settings

- **Features**
  - ✅ Enable Issues
  - ✅ Enable Discussions (for community support)
  - ❌ Disable Wiki (reduces attack surface; use docs/ instead)
  - ❌ Disable Projects (unless actively used)

- **Pull Requests**
  - ✅ Allow squash merging (recommended)
  - ❌ Disable merge commits (prevents accidental merges)
  - ❌ Disable rebase merging (optional, based on workflow preference)
  - ✅ Always suggest updating pull request branches
  - ✅ Automatically delete head branches

- **Archives**
  - ❌ Do not enable "Include Git LFS objects in archives"

#### Security Settings
Navigate to: https://github.com/redevops-io/ingress-nginx/settings/security_analysis

- **Private vulnerability reporting**
  - ✅ Enable private vulnerability reporting

- **Dependabot**
  - ✅ Enable Dependabot alerts
  - ✅ Enable Dependabot security updates
  - ❌ Disable Dependabot version updates (creates noise; update manually on schedule)

- **Code scanning**
  - ✅ Enable CodeQL analysis for Go code
  - Add Trivy or Snyk for container scanning once images are published

- **Secret scanning**
  - ✅ Enable secret scanning
  - ✅ Enable push protection

#### Actions Settings
Navigate to: https://github.com/redevops-io/ingress-nginx/settings/actions

- **Actions permissions**
  - Select: "Allow all actions and reusable workflows"
  - Or: "Allow redevops-io actions and verified actions" (more restrictive)

- **Workflow permissions**
  - ✅ Read repository contents and packages permissions
  - ❌ Disable "Read and write permissions" by default
  - ✅ Allow GitHub Actions to create and approve pull requests (if using Dependabot)

- **Artifact and log retention**
  - Set to `90 days` (balance between debugging and storage costs)

## Access Control

### Collaborators
Navigate to: https://github.com/redevops-io/ingress-nginx/settings/access

Only add trusted users with appropriate permission levels:

- **Admin**: Full access (very few users)
- **Maintain**: Manage repository without destructive actions (core maintainers)
- **Write**: Push to branches but not master (active contributors)
- **Triage**: Manage issues and PRs (community moderators)
- **Read**: View only (external auditors, security researchers)

### Teams (if using GitHub Organizations)
Create teams like:
- `@redevops-io/ingress-maintainers` (Admin/Maintain)
- `@redevops-io/ingress-contributors` (Write)
- `@redevops-io/ingress-triagers` (Triage)

## Monitoring

### Audit Log
Regularly review: https://github.com/redevops-io/ingress-nginx/settings/audit-log

Watch for:
- Unexpected branch protection changes
- New collaborators added
- Secret scanning alerts
- Large commits or force pushes

### GitHub Apps & Integrations
Review installed apps: https://github.com/redevops-io/ingress-nginx/settings/installations

Only allow:
- GitHub Actions (built-in)
- Trusted CI/CD tools (if needed)
- Approved security scanners

## Incident Response

If unauthorized changes occur:

1. **Immediately revert** using `git revert` or force-push after backing up:
   ```bash
   git fetch origin
   git reset --hard origin/master~N  # N = number of bad commits
   git push --force-with-lease origin master
   ```

2. **Review access logs** to identify the source

3. **Remove compromised credentials/keys**:
   - Rotate deploy keys
   - Revoke personal access tokens
   - Update GitHub App installations

4. **Re-apply branch protection** if settings were changed

5. **Notify the team** via Slack/email

6. **File a security incident report** with details

## Signed Commits

Require all commits to be GPG/SSH signed:

### For Contributors
```bash
# Configure Git to sign commits
git config --global user.signingkey <YOUR_GPG_KEY_ID>
git config --global commit.gpgsign true

# Or use SSH signing (GitHub now supports this)
git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/id_ed25519.pub
```

### For Maintainers
Enable "Require signed commits" in branch protection rules and reject any unsigned PRs.

## Workflow File Protection

GitHub Actions workflows in `.github/workflows/` are powerful and can be attack vectors.

### Best Practices
1. **Pin action versions** by full SHA (already done in your workflows)
2. **Review PRs changing workflows** extra carefully
3. **Limit workflow permissions** to minimum required (already configured)
4. **Use CODEOWNERS** to require maintainer approval for workflow changes:

   Create `.github/CODEOWNERS`:
   ```
   # Require maintainer review for sensitive paths
   /.github/workflows/ @redevops-io/ingress-maintainers
   /SECURITY.md @redevops-io/ingress-maintainers
   /go.mod @redevops-io/ingress-maintainers
   /go.sum @redevops-io/ingress-maintainers
   ```

5. **Disable automatic workflow runs** for first-time contributors:
   - Go to Actions settings
   - Select "Require approval for first-time contributors"

## Summary Checklist

- [ ] Enable branch protection on `master`
- [ ] Require pull request reviews (1+ approvals)
- [ ] Require status checks to pass
- [ ] Disable force pushes and branch deletion
- [ ] Enable signed commits
- [ ] Restrict direct push access to master
- [ ] Enable private vulnerability reporting
- [ ] Enable Dependabot alerts
- [ ] Enable secret scanning with push protection
- [ ] Enable CodeQL scanning
- [ ] Set minimum workflow permissions
- [ ] Add CODEOWNERS file
- [ ] Review collaborator access regularly
- [ ] Monitor audit log monthly
- [ ] Document incident response plan

---

For questions or to report security issues, contact `support@redevops.io`.
