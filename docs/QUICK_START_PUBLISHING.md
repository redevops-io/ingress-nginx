# Quick Start Guide: Publishing Your First Image Set

This guide walks you through publishing the initial set of container images for independent fork operation.

## Prerequisites

1. **GitHub Personal Access Token** with `write:packages` permission
   - Create at: https://github.com/settings/tokens/new
   - Required scopes: `write:packages`, `delete:packages`, `read:packages`

2. **Add Repository Secrets**:
   ```bash
   # Go to: https://github.com/redevops-io/ingress-nginx/settings/secrets/actions
   # Add these secrets:
   GHCR_TOKEN=<your_personal_access_token>
   ```

3. **Docker with buildx** (for multi-arch builds)
   ```bash
   docker buildx version
   docker buildx create --name multiarch --use
   ```

## Option 1: Automated (Recommended)

### Using GitHub Actions

1. **Create and push a version tag**:
   ```bash
   cd /projects/ingress-nginx
   
   # Create a release tag
   export VERSION=v1.14.0-redevops.1
   git tag -s controller-${VERSION} -m "Initial fork release ${VERSION}"
   git push origin controller-${VERSION}
   ```

2. **The workflow will automatically**:
   - Build NGINX base image
   - Build controller and controller-chroot images
   - Build all 8 support images
   - Push to `ghcr.io/redevops-io/ingress-nginx/*`
   - Create GitHub release with notes

3. **Monitor the build**:
   - Go to: https://github.com/redevops-io/ingress-nginx/actions
   - Watch the "Publish Container Images" workflow
   - Build time: ~30-45 minutes (multi-arch)

4. **After successful build**:
   - Images will be at: https://github.com/orgs/redevops-io/packages
   - Set each package visibility to **Public**

## Option 2: Manual Build

### Step 1: Build NGINX Base Image

```bash
cd /projects/ingress-nginx

# Login to GitHub Container Registry
echo $GHCR_TOKEN | docker login ghcr.io -u YOUR_GITHUB_USERNAME --password-stdin

# Build and push NGINX base (multi-arch)
cd images/nginx/rootfs
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --push \
  -t ghcr.io/redevops-io/ingress-nginx/nginx:v2.2.5 \
  -t ghcr.io/redevops-io/ingress-nginx/nginx:latest \
  .

# Get the image digest
NGINX_DIGEST=$(docker buildx imagetools inspect ghcr.io/redevops-io/ingress-nginx/nginx:v2.2.5 --format '{{json .}}' | jq -r .manifest.digest)
echo "NGINX digest: ${NGINX_DIGEST}"

# Update NGINX_BASE file
cd ../../..
echo "ghcr.io/redevops-io/ingress-nginx/nginx:v2.2.5@${NGINX_DIGEST}" > NGINX_BASE
```

### Step 2: Build Controller Images

```bash
cd /projects/ingress-nginx

# Set version
export VERSION=v1.14.0-redevops.1
export REGISTRY=ghcr.io/redevops-io/ingress-nginx

# Update TAG file
echo ${VERSION} > TAG

# Build controller (multi-arch)
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --build-arg BASE_IMAGE=$(cat NGINX_BASE) \
  --build-arg VERSION=${VERSION} \
  --push \
  -t ${REGISTRY}/controller:${VERSION} \
  -t ${REGISTRY}/controller:latest \
  rootfs

# Build controller-chroot (multi-arch)
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --build-arg BASE_IMAGE=$(cat NGINX_BASE) \
  --build-arg VERSION=${VERSION} \
  --push \
  -t ${REGISTRY}/controller-chroot:${VERSION} \
  -t ${REGISTRY}/controller-chroot:latest \
  -f rootfs/Dockerfile-chroot \
  rootfs
```

### Step 3: Build Support Images

```bash
cd /projects/ingress-nginx/images

# Build kube-webhook-certgen
cd kube-webhook-certgen
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --push \
  -t ghcr.io/redevops-io/ingress-nginx/kube-webhook-certgen:v1.4.1 \
  -t ghcr.io/redevops-io/ingress-nginx/kube-webhook-certgen:latest \
  rootfs

# Build custom-error-pages
cd ../custom-error-pages
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --push \
  -t ghcr.io/redevops-io/ingress-nginx/custom-error-pages:0.7 \
  -t ghcr.io/redevops-io/ingress-nginx/custom-error-pages:latest \
  .

# Build e2e-test-echo
cd ../e2e-test-echo
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --push \
  -t ghcr.io/redevops-io/ingress-nginx/e2e-test-echo:latest \
  .

# Build httpbun
cd ../httpbun
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --push \
  -t ghcr.io/redevops-io/ingress-nginx/httpbun:latest \
  .

# Build ext-auth-example-authsvc
cd ../ext-auth-example-authsvc
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --push \
  -t ghcr.io/redevops-io/ingress-nginx/ext-auth-example-authsvc:latest \
  .

# Build cfssl
cd ../cfssl
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --push \
  -t ghcr.io/redevops-io/ingress-nginx/cfssl:latest \
  .

# Build fastcgi-helloserver
cd ../fastcgi-helloserver
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --push \
  -t ghcr.io/redevops-io/ingress-nginx/fastcgi-helloserver:latest \
  .

# Build go-grpc-greeter-server
cd ../go-grpc-greeter-server
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --push \
  -t ghcr.io/redevops-io/ingress-nginx/go-grpc-greeter-server:latest \
  .
```

### Step 4: Verify Images

```bash
# List all published images
curl -H "Authorization: Bearer $GHCR_TOKEN" \
  https://ghcr.io/v2/redevops-io/ingress-nginx/controller/tags/list

# Pull and test controller image
docker pull ghcr.io/redevops-io/ingress-nginx/controller:v1.14.0-redevops.1
docker run --rm ghcr.io/redevops-io/ingress-nginx/controller:v1.14.0-redevops.1 --version

# Verify all critical images exist
for img in controller controller-chroot nginx kube-webhook-certgen custom-error-pages; do
  echo "Checking ${img}..."
  docker manifest inspect ghcr.io/redevops-io/ingress-nginx/${img}:latest && echo "✅ ${img}" || echo "❌ ${img}"
done
```

## Step 5: Update Repository References

### Commit Updated Files

```bash
cd /projects/ingress-nginx

# Commit the updated NGINX_BASE and TAG
git add NGINX_BASE TAG Makefile
git commit -m "Update registry to ghcr.io/redevops-io for independent operation

- Changed REGISTRY in Makefile to ghcr.io/redevops-io/ingress-nginx
- Updated NGINX_BASE to point to fork's nginx base image
- Bumped TAG to ${VERSION} for initial fork release"

git push origin master
```

### Update Helm Chart (Optional)

```bash
cd charts/ingress-nginx

# Edit values.yaml
sed -i 's|registry.k8s.io/ingress-nginx|ghcr.io/redevops-io/ingress-nginx|g' values.yaml
sed -i "s|tag: .*|tag: ${VERSION}|g" values.yaml

# Edit Chart.yaml
sed -i "s|version: .*|version: ${VERSION}|g" Chart.yaml
sed -i "s|appVersion: .*|appVersion: ${VERSION}|g" Chart.yaml

# Test the chart
helm lint .
helm template test-release . --dry-run

# Commit changes
git add values.yaml Chart.yaml
git commit -m "Update Helm chart to use fork's registry"
git push origin master
```

## Step 6: Test Installation

### Test with Kind

```bash
# Create kind cluster
kind create cluster --name test-ingress

# Install from your fork's images
kubectl apply -f https://raw.githubusercontent.com/redevops-io/ingress-nginx/master/deploy/static/provider/kind/deploy.yaml

# Wait for controller to be ready
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=120s

# Check controller version
kubectl exec -n ingress-nginx deploy/ingress-nginx-controller -- /nginx-ingress-controller --version

# Deploy test application
kubectl create deployment demo --image=nginx:alpine
kubectl expose deployment demo --port=80
kubectl create ingress demo --class=nginx --rule="demo.localdev.me/*=demo:80"

# Test ingress
curl http://localhost/

# Cleanup
kind delete cluster --name test-ingress
```

### Test with Helm

```bash
# Add local repo
helm repo add ingress-nginx file://$(pwd)/charts/ingress-nginx
helm repo update

# Install
helm install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-nginx --create-namespace \
  --set controller.image.registry=ghcr.io \
  --set controller.image.image=redevops-io/ingress-nginx/controller \
  --set controller.image.tag=${VERSION}

# Check status
helm status ingress-nginx -n ingress-nginx
kubectl get pods -n ingress-nginx

# Uninstall
helm uninstall ingress-nginx -n ingress-nginx
```

## Step 7: Make Packages Public

1. Go to: https://github.com/orgs/redevops-io/packages
2. For each package (controller, nginx, kube-webhook-certgen, etc.):
   - Click on the package
   - Go to "Package settings"
   - Scroll to "Danger Zone"
   - Click "Change visibility" → "Public"
   - Confirm the change

## Troubleshooting

### Build Fails: Permission Denied

```bash
# Make sure you're logged in
echo $GHCR_TOKEN | docker login ghcr.io -u YOUR_USERNAME --password-stdin

# Check token has correct permissions
curl -H "Authorization: Bearer $GHCR_TOKEN" https://ghcr.io/v2/
```

### Image Push Fails: Unauthorized

- Verify `GHCR_TOKEN` secret is set in repository
- Check token has `write:packages` scope
- Ensure repository name matches: `redevops-io/ingress-nginx`

### Multi-arch Build Not Working

```bash
# Setup buildx
docker buildx create --name multiarch --use
docker buildx inspect --bootstrap

# If still failing, build single-arch first
docker buildx build --platform linux/amd64 --load -t test:latest .
```

### Workflow Doesn't Trigger

- Check `.github/workflows/publish-images.yaml` exists
- Verify tag name starts with `controller-v`
- Ensure you pushed the tag: `git push origin controller-v1.14.0-redevops.1`

### Images Not Visible After Push

- Wait 1-2 minutes for registry indexing
- Make packages public (see Step 7)
- Check: https://github.com/orgs/redevops-io/packages

## Next Steps

After successfully publishing images:

1. ✅ **Enable Security Scanning**
   - The `security-scan.yaml` workflow will now work
   - Images will be scanned daily for vulnerabilities

2. ✅ **Set Up Dependabot**
   - Go to: https://github.com/redevops-io/ingress-nginx/settings/security_analysis
   - Enable "Dependabot alerts" and "Dependabot security updates"

3. ✅ **Configure Branch Protection**
   - Implement rules from `docs/REPOSITORY_PROTECTION.md`
   - Require status checks to pass before merging

4. ✅ **Schedule Kubernetes Compatibility Tests**
   - The `k8s-compatibility.yaml` workflow will run monthly
   - Manually trigger first run to verify setup

5. ✅ **Document Release Process**
   - Update `CONTRIBUTING.md` with versioning strategy
   - Create release checklist template

6. ✅ **Announce Fork Availability**
   - Update README.md with installation instructions
   - Post in relevant communities (if applicable)

## Success Checklist

- [ ] All 11 images built and pushed to ghcr.io
- [ ] Packages made public on GitHub
- [ ] NGINX_BASE file updated with fork's nginx image
- [ ] TAG file updated with fork version
- [ ] Makefile REGISTRY updated to ghcr.io/redevops-io/ingress-nginx
- [ ] Changes committed and pushed
- [ ] Helm chart tested with new images
- [ ] Kind cluster test successful
- [ ] Security scanning workflow enabled
- [ ] GitHub release created (if using automated method)
- [ ] Documentation updated with fork-specific info

---

**Congratulations!** 🎉 Your fork is now independently operational with its own container images.

For ongoing maintenance, see:
- `docs/INDEPENDENT_OPERATION.md` - Complete maintenance guide
- `.github/workflows/` - Automated workflows for builds, tests, scans
- `SECURITY.md` - Security policy and vulnerability reporting
