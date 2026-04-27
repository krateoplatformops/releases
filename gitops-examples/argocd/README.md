# Argo CD Job Templates

This folder contains plain Kubernetes manifests showing one way to use Argo CD to manage a Krateo installation inside the cluster.

> [!NOTE]
> These manifests are sample-only examples. If you need to personalize the Jobs for a specific set of needs, such as installing with a specific override profile, edit them to match those needs and publish them in a separate repository or in a fork of this one.

Each manifest is a plain Kubernetes `Job` that uses the official `krateoctl` container image directly and then runs `krateoctl install apply`. The Job uses the pod's ServiceAccount credentials, so no kubeconfig Secret is needed.

## Structure

```
gitops-examples/argocd/
├── ingress/
│   └── job.yaml
├── loadbalancer/
│   └── job.yaml
└── nodeport/
    └── job.yaml
```

Supported install types:

- `nodeport`
- `loadbalancer`
- `ingress`

## Notes

- Deploy one install type per cluster.
- The Job depends on the `krateoctl-install` ServiceAccount and its ClusterRoleBinding in `krateo-system`.