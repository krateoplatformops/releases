#!/bin/bash
# Usage: ./scripts/release.sh 3.0.0-rc2-dev11
set -e

VERSION=$1
SEMVER_RE='^[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9]+)*$'

if [[ -z "$VERSION" ]]; then
  echo "Usage: $0 <version>  (e.g. $0 3.0.0  or  $0 3.0.0-rc2  or  $0 3.0.0-alpha1-dev11)"
  exit 1
fi

if [[ ! "$VERSION" =~ $SEMVER_RE ]]; then
  echo "✗ Invalid version format: '${VERSION}'"
  echo "  Expected: X.Y.Z[-<label>...]  (e.g. 3.0.0, 3.0.0-rc2, 3.0.0-alpha1-dev11)"
  exit 1
fi

echo "→ Substituting RELEASE_VERSION with ${VERSION}..."
sed -i "s/RELEASE_VERSION/${VERSION}/g" \
  argocd/jobs/ingress/job.yaml \
  argocd/jobs/loadbalancer/job.yaml \
  argocd/jobs/nodeport/job.yaml

echo "→ Committing..."
git add argocd/jobs/ingress/job.yaml \
        argocd/jobs/loadbalancer/job.yaml \
        argocd/jobs/nodeport/job.yaml
git commit -m "release: ${VERSION}"

echo "→ Tagging ${VERSION}..."
git tag "${VERSION}"

echo "→ Pushing..."
git push origin main "${VERSION}"

echo ""
echo "✓ Released ${VERSION}"
