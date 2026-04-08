# Argo CD Job Templates

This folder contains reusable Kubernetes Job assets intended for the GitOps repository that launches `krateoctl` from Argo CD.

## What is included

- Three self-contained YAML manifests, one for each install type:
  - `nodeport`
  - `loadbalancer`
  - `ingress`

## How to use it

Each manifest is a plain Kubernetes `Job`, so it can be applied without Kustomize.
At runtime the Job uses the official `krateoctl` container image directly and runs `krateoctl install apply`.
The Job expects a mounted Secret named `krateoctl-kubeconfig` with a `config` key available at `/kubeconfig/config`.

If you are using Argo CD, point the Application at one of:

- `argocd/jobs/nodeport/job.yaml`
- `argocd/jobs/loadbalancer/job.yaml`
- `argocd/jobs/ingress/job.yaml`

The Job exits with a non-zero code if `krateoctl install apply` fails, so Kubernetes and Argo CD can surface the failure immediately.
The release version is embedded in the Job command, so when the GitOps repo updates to a new release the Job template changes and the controller can recreate it cleanly.

If you want controller-level examples for the GitOps repository, see [`gitops-examples/`](../../gitops-examples/README.md).

## Notes

- RBAC is intentionally not defined here. It belongs in the GitOps repository, as requested.
- The release repository stays focused on versioned installation assets consumed by `krateoctl`.
- If you need a different release version, update the version string in the Job command and keep the GitOps controller set to recreate immutable Jobs.
- Make sure the GitOps repo creates the `krateoctl-kubeconfig` Secret in the target namespace before the Job runs.
