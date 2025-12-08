# Independent Fork Operation Guide

This guide explains how to operate the redevops-io/ingress-nginx fork independently after the upstream kubernetes/ingress-nginx repository is decommissioned.

## Overview

To operate independently, you need to:

1. **Publish container images** to your own registry (GitHub Container Registry)
2. **Run periodic tests** to ensure compatibility with new Kubernetes versions
3. **Set up automated workflows** for builds, tests, and releases
4. **Monitor security vulnerabilities** in dependencies and base images

## Container Images Architecture

### Images You Need to Publish

The ingress-nginx controller requires **11 container images**:

#### Primary Images (Critical)

1. **Controller Image** (`ghcr.io/redevops-io/ingress-nginx/controller`)
   - The main ingress-nginx controller binary
   - Built from: `rootfs/Dockerfile`
   - Multi-arch: `linux/amd64`, `linux/arm64`
   - **This is the most important image**

2. **Controller Chroot Image** (`ghcr.io/redevops-io/ingress-nginx/controller-chroot`)
   - Hardened version with chroot isolation
   - Built from: `rootfs/Dockerfile-chroot`
   - Multi-arch: `linux/amd64`, `linux/arm64`
   - Recommended for production

3. **NGINX Base Image** (`ghcr.io/redevops-io/ingress-nginx/nginx`)
   - Custom-built NGINX with OpenTelemetry, ModSecurity, etc.
   - Built from: `images/nginx/rootfs/Dockerfile`
   - Base image for the controller
   - Currently using: `v2.2.5`

#### Support Images (for testing and examples)

4. **kube-webhook-certgen** (`ghcr.io/redevops-io/ingress-nginx/kube-webhook-certgen`)
   - Generates TLS certificates for admission webhook
   - Required for production installations
   - Built from: `images/kube-webhook-certgen/`

5. **custom-error-pages** (`ghcr.io/redevops-io/ingress-nginx/custom-error-pages`)
   - Default error page backend
   - Built from: `images/custom-error-pages/`

6. **e2e-test-echo** (`ghcr.io/redevops-io/ingress-nginx/e2e-test-echo`)
   - Echo server for e2e tests
   - Built from: `images/e2e-test-echo/`

7. **httpbun** (`ghcr.io/redevops-io/ingress-nginx/httpbun`)
   - HTTP testing service
   - Built from: `images/httpbun/`

8. **ext-auth-example-authsvc** (`ghcr.io/redevops-io/ingress-nginx/ext-auth-example-authsvc`)
   - Example external authentication service
   - Built from: `images/ext-auth-example-authsvc/`

9. **cfssl** (`ghcr.io/redevops-io/ingress-nginx/cfssl`)
   - Certificate authority for testing
   - Built from: `images/cfssl/`

10. **fastcgi-helloserver** (`ghcr.io/redevops-io/ingress-nginx/fastcgi-helloserver`)
    - FastCGI test backend
    - Built from: `images/fastcgi-helloserver/`

11. **go-grpc-greeter-server** (`ghcr.io/redevops-io/ingress-nginx/go-grpc-greeter-server`)
    - gRPC test backend
    - Built from: `images/go-grpc-greeter-server/`

### Image Dependencies

```
nginx base image (v2.2.5)
    ↓
controller image (v1.14.0)
    ↓
controller-chroot image (v1.14.0)

kube-webhook-certgen ← used during installation
custom-error-pages   ← default backend
test images          ← e2e test suite
```

## Registry Setup

### GitHub Container Registry (ghcr.io)

**Recommended**: Use GitHub Container Registry (free for public repos)

#### Setup Steps

1. **Create GitHub Personal Access Token** with `write:packages` permission:
   - Go to: https://github.com/settings/tokens/new
   - Scopes: `write:packages`, `delete:packages`, `read:packages`
   - Save as repository secret: `GHCR_TOKEN`

2. **Add Repository Secrets**:
   - Go to: https://github.com/redevops-io/ingress-nginx/settings/secrets/actions
   - Add:
     - `GHCR_TOKEN`: Your personal access token
     - `GHCR_USERNAME`: Your GitHub username (e.g., `redevops-io`)

3. **Configure Package Visibility**:
   - After first push, go to: https://github.com/orgs/redevops-io/packages
   - For each package, set visibility to **Public**

### Alternative: Docker Hub

If you prefer Docker Hub:

1. Create Docker Hub account/organization
2. Add secrets:
   - `DOCKERHUB_USERNAME`
   - `DOCKERHUB_TOKEN`
3. Update registry in workflows to `docker.io/redevops`

## Publishing Workflows

See `.github/workflows/publish-images.yaml` (to be created) for the automated workflow.

### Manual Publishing (Initial Setup)

For the first release, build and push manually:

```bash
# 1. Build NGINX base image
cd images/nginx/rootfs
export TAG=v2.2.5
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --push \
  -t ghcr.io/redevops-io/ingress-nginx/nginx:${TAG} \
  .

# 2. Update NGINX_BASE file
cd ../../..
echo "ghcr.io/redevops-io/ingress-nginx/nginx:${TAG}@sha256:..." > NGINX_BASE

# 3. Build controller images
export VERSION=v1.14.0-redevops.1
export REGISTRY=ghcr.io/redevops-io/ingress-nginx
make BASE_IMAGE=ghcr.io/redevops-io/ingress-nginx/nginx:${TAG} \
  TAG=${VERSION} \
  ARCH=amd64 \
  image

# 4. Build multi-arch and push
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --build-arg BASE_IMAGE=ghcr.io/redevops-io/ingress-nginx/nginx:${TAG} \
  --build-arg VERSION=${VERSION} \
  --push \
  -t ${REGISTRY}/controller:${VERSION} \
  rootfs

# 5. Build chroot variant
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --build-arg BASE_IMAGE=ghcr.io/redevops-io/ingress-nginx/nginx:${TAG} \
  --build-arg VERSION=${VERSION} \
  --push \
  -t ${REGISTRY}/controller-chroot:${VERSION} \
  rootfs -f rootfs/Dockerfile-chroot

# 6. Build support images
cd images
for img in kube-webhook-certgen custom-error-pages e2e-test-echo httpbun ext-auth-example-authsvc cfssl fastcgi-helloserver go-grpc-greeter-server; do
  make NAME=$img REGISTRY=ghcr.io/redevops-io/ingress-nginx build push
done
```

## Versioning Strategy

### Format: `vMAJOR.MINOR.PATCH-redevops.BUILD`

Example: `v1.14.0-redevops.1`

- `v1.14.0`: Tracks upstream version compatibility
- `redevops.1`: Your fork's build number

### When to Increment

- **MAJOR.MINOR**: When rebasing on a new upstream release
- **PATCH**: For bug fixes maintaining compatibility
- **BUILD**: For each build/release (security patches, dependency updates)

### Git Tagging

Create tags for each release:

```bash
git tag -s controller-v1.14.0-redevops.1 -m "Release v1.14.0-redevops.1"
git push origin controller-v1.14.0-redevops.1
```

## Testing Strategy

### Periodic Test Schedule

| Test Type | Frequency | When to Run |
|-----------|-----------|-------------|
| Unit Tests | Every commit | CI on PR/push |
| Lint/Static Analysis | Every commit | CI on PR/push |
| e2e Tests (short) | Every PR | CI on PR |
| e2e Tests (full) | Weekly | Monday 9 AM UTC |
| Multi-arch Build Test | Every release | Release workflow |
| K8s Compatibility | Monthly | 1st of month |
| Dependency Scan | Weekly | Monday 9 AM UTC |
| CVE Scan | Daily | 2 AM UTC |

### Kubernetes Compatibility Matrix

Test against:

- **Current stable**: v1.34
- **Previous stable**: v1.33
- **Two versions back**: v1.32

Update monthly as new K8s versions are released.

### Test Execution

#### Local Testing

```bash
# Unit tests
make test

# Lint checks
make static-check

# Build verification
make build

# e2e tests (requires kind cluster)
make kind-e2e-test
```

#### CI Testing (Automated)

See `.github/workflows/` for:
- `ci.yaml` - Run on every PR
- `k8s-compatibility.yaml` - Monthly compatibility tests
- `security-scan.yaml` - Daily vulnerability scans

## Maintenance Workflows

### Weekly Tasks

1. **Review Dependabot PRs** for Go module updates
2. **Check CVE dashboards** for new vulnerabilities
3. **Run full e2e test suite** against latest K8s
4. **Review open issues** from community

### Monthly Tasks

1. **Test against new K8s release candidates**
2. **Update compatibility matrix** in README.md
3. **Review and update dependencies**
4. **Check for NGINX updates** (OpenResty, modules)
5. **Audit access logs** for suspicious activity

### Quarterly Tasks

1. **Rebase on upstream** if still active (or cherry-pick important fixes)
2. **Security audit** of fork-specific changes
3. **Performance testing** and benchmarking
4. **Documentation review** and updates
5. **Community survey** (if applicable)

### On-Demand Tasks

1. **Emergency CVE response** (within 24-48 hours)
2. **Critical bug fixes** from issue reports
3. **K8s API deprecation** handling
4. **Major feature requests** evaluation

## Monitoring and Alerting

### What to Monitor

1. **GitHub Actions Status**
   - CI/CD workflow failures
   - Scheduled test results
   - Dependency update PRs

2. **Security Alerts**
   - Dependabot alerts
   - CVE database (NVD, GitHub Security Advisories)
   - NGINX/OpenResty security lists

3. **Image Registry**
   - Pull counts (usage metrics)
   - Storage usage
   - Bandwidth costs

4. **Community Health**
   - Issue response time
   - PR review time
   - Discussion activity

### Alert Configuration

Set up notifications for:

- **Critical**: Security vulnerabilities, workflow failures
- **High**: New Kubernetes release, failed e2e tests
- **Medium**: Stale PRs, dependency updates available
- **Low**: Weekly test summaries, usage metrics

## Release Process

### 1. Prepare Release

```bash
# Checkout clean master
git checkout master
git pull origin master

# Create release branch
export VERSION=v1.14.0-redevops.2
git checkout -b release-${VERSION}

# Update version files
echo ${VERSION} > TAG
git add TAG
git commit -m "Bump version to ${VERSION}"
```

### 2. Run Pre-Release Tests

```bash
# Full test suite
make test
make static-check

# Build all images locally
make build image image-chroot

# Run e2e tests
cd test/e2e
go test -v ./...
```

### 3. Build and Push Images

```bash
# Will be automated by workflow
git push origin release-${VERSION}

# Tag the release
git tag -s controller-${VERSION} -m "Release ${VERSION}"
git push origin controller-${VERSION}
```

### 4. Update Helm Chart

```bash
cd charts/ingress-nginx

# Update Chart.yaml version
# Update values.yaml with new image tags

helm package .
helm repo index .
```

### 5. Create GitHub Release

1. Go to: https://github.com/redevops-io/ingress-nginx/releases/new
2. Select tag: `controller-${VERSION}`
3. Title: "ingress-nginx ${VERSION}"
4. Description: Changelog, breaking changes, upgrade notes
5. Attach: Helm chart, checksums, signatures
6. Publish

### 6. Announce Release

- Post in `#redevops-ingress` Slack
- Update README.md compatibility table
- Send email to users list (if exists)
- Tweet from @redevops account

## Cost Considerations

### GitHub Actions

- **Free tier**: 2,000 minutes/month for public repos
- **Estimated usage**: ~500-800 minutes/month
- **Strategy**: Use self-hosted runners if exceeding limit

### Container Registry

- **GitHub Container Registry**: Free for public packages
- **Storage**: ~10-20 GB total (all images, all tags)
- **Bandwidth**: Free for public access

### Infrastructure

- **Test clusters**: Use kind/k3s (local, free)
- **CI runners**: GitHub-hosted (included)
- **Monitoring**: GitHub insights (free)

**Total estimated cost**: $0-20/month (depending on runner needs)

## Emergency Procedures

### Critical CVE Response

1. **Assess impact** (< 2 hours)
2. **Create hotfix branch** from latest tag
3. **Apply fix** and add regression test
4. **Emergency release** with bumped BUILD number
5. **Publish security advisory** on GitHub
6. **Notify users** via all channels

### Workflow Failure

1. Check GitHub Actions logs
2. Re-run failed jobs if transient
3. File issue if persistent
4. Disable workflow if blocking releases

### Image Registry Issues

1. Switch to Docker Hub as backup
2. Update workflows to use alternate registry
3. Notify users of new image location

## Summary Checklist

Before going independent:

- [ ] Set up GitHub Container Registry access
- [ ] Configure repository secrets (GHCR_TOKEN)
- [ ] Create publishing workflows
- [ ] Build and push initial image set
- [ ] Update NGINX_BASE to your registry
- [ ] Enable branch protection rules
- [ ] Set up security scanning
- [ ] Configure Dependabot
- [ ] Document fork status in README
- [ ] Create first tagged release
- [ ] Test Helm chart with new images
- [ ] Set up monitoring/alerts
- [ ] Establish release schedule

---

**Next Steps**: See the workflow files being created:
- `.github/workflows/publish-images.yaml` - Automated image building/publishing
- `.github/workflows/k8s-compatibility.yaml` - Monthly K8s version testing
- `.github/workflows/security-scan.yaml` - Daily vulnerability scanning
