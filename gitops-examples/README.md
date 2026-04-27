# GitOps Examples

These manifests are concrete examples for the GitOps repository that applies the `krateoctl` install Job on the `argo-job-testing` branch of this repo.

They are intentionally separate from the release assets and show how to wire the same plain YAML workload with either:

- Argo CD
- Flux

Argo CD examples live under [`argocd/`](./argocd/) and Flux examples live under their own example path.

The examples are already filled in for the current repository and branch. Because the repo is public, no SSH key or repository secret is needed.

Argo CD will recreate the Job on updates because the Application uses `Replace=true`.
Flux will recreate the Job on immutable changes because the Kustomization uses `force: true`.

If you copy them into another GitOps repo, change:

- the repo URL
- the path
- the install type if you want `nodeport` or `ingress`
- the release version string in the Job command

Default install type in these examples:

- `nodeport`

Supported install types:

- `nodeport`
- `loadbalancer`
- `ingress`
