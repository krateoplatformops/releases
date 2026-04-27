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

echo "→ Updating version to ${VERSION} in job manifests..."
for f in gitops-examples/argocd/ingress/job.yaml \
         gitops-examples/argocd/loadbalancer/job.yaml \
         gitops-examples/argocd/nodeport/job.yaml; do
  # Update version labels
  sed -i.bak "s/app.kubernetes.io\/version:.*/app.kubernetes.io\/version: ${VERSION}/" "$f"
  # Update --version arg (the line immediately after "- --version")
  sed -i.bak '/- --version/{n; s/.*/            - "'"${VERSION}"'"/;}' "$f"
  # Clean up the backup file
  rm -f "${f}.bak"
done