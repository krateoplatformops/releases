# GitOps Examples

These manifests are examples for the GitOps repository that applies the `krateoctl` install Job.

They are intentionally separate from the release assets and show how to wire the same plain YAML workload with either:

- Argo CD
- Flux

Replace the placeholders before copying them into the GitOps repository:

- `__GITOPS_REPO_URL__`
- `__GITOPS_PATH__`
- `__INSTALL_TYPE__`

Supported install types:

- `nodeport`
- `loadbalancer`
- `ingress`
