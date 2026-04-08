# Argo CD Job Templates

This folder contains reusable Kubernetes Job assets intended for the GitOps repository that launches `krateoctl` from Argo CD.

## What is included

- Three self-contained YAML manifests, one for each install type:
  - `nodeport`
  - `loadbalancer`
  - `ingress`

## How to use it

Each manifest contains both the `ConfigMap` and the `Job`, so it can be applied without Kustomize.

If you are using Argo CD, point the Application at one of:

- `argocd/jobs/nodeport/job.yaml`
- `argocd/jobs/loadbalancer/job.yaml`
- `argocd/jobs/ingress/job.yaml`

Required keys:

- `KRATEOCTL_VERSION`
- `KRATEOCTL_REPOSITORY`
- `KRATEOCTL_NAMESPACE`
- `KRATEOCTL_TYPE`

The Job exits with a non-zero code if `krateoctl install apply` fails, so Kubernetes and Argo CD can surface the failure immediately.
The resource names include the release tag placeholder, so when the GitOps repo updates to a new release the Job is recreated rather than patched in place.

If you want controller-level examples for the GitOps repository, see [`gitops-examples/`](../../gitops-examples/README.md).

## Notes

- RBAC is intentionally not defined here. It belongs in the GitOps repository, as requested.
- The release repository stays focused on versioned installation assets consumed by `krateoctl`.
- Replace `__SET_RELEASE_TAG__` with the actual release tag in the GitOps repository.
