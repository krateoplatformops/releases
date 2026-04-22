# Argo CD Job Templates

This folder contains plain Kubernetes manifests — one `Job` per install type. No Helm, no Kustomize. The releases repository stays pure YAML.

## Structure

```
argocd/jobs/
├── ingress/
│   └── job.yaml      # ServiceAccount + ClusterRoleBinding + Job (ingress)
├── loadbalancer/
│   └── job.yaml      # ServiceAccount + ClusterRoleBinding + Job (loadbalancer)
└── nodeport/
    └── job.yaml      # ServiceAccount + ClusterRoleBinding + Job (nodeport)
```

Each manifest is self-contained and can be applied directly with `kubectl apply -f` if needed.

## Prerequisites

No kubeconfig Secret is required. The Job runs with the `krateoctl-install` ServiceAccount and uses in-cluster Kubernetes credentials.

## ArgoCD Application (GitOps repository)

Deploy **one** install type per cluster. In your GitOps repository, create a single `Application` and set `path` to the install type you need.

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: krateo-install
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/krateoplatformops/releases
    targetRevision: HEAD
    path: argocd/jobs/ingress   # ← change to: ingress | loadbalancer | nodeport
  destination:
    server: https://kubernetes.default.svc
    namespace: krateo-system
  syncPolicy:
    automated:
      prune: true
      selfHeal: false
    syncOptions:
      - CreateNamespace=true
```

That's the only field you ever need to change.

## How it works

1. ArgoCD syncs the `Application` and reads the plain YAML from the chosen path.
2. Kubernetes creates the `Job` in the target namespace.
3. The `krateoctl` container runs `krateoctl install apply --type <installType> ...` using the pod's ServiceAccount.
4. The Job exits with a non-zero code on failure, surfacing errors immediately in ArgoCD.
5. After 300 seconds the completed Job is automatically garbage-collected.

## Notes

- `selfHeal: false` is intentional — Jobs are immutable once created. ArgoCD should not attempt to reconcile a running or completed Job.
- To re-run the installation (e.g. after a version bump), delete the old Job manually or let `ttlSecondsAfterFinished` expire, then trigger a new sync.
- The Job depends on the `krateoctl-install` ServiceAccount and its ClusterRoleBinding in `krateo-system`.