# Krateo Release Configurations

> [!IMPORTANT]
> This repository is intended **exclusively for use with `krateoctl`**. These configuration files are not meant to be used directly with `kubectl` or other deployment tools. Always use the `krateoctl` CLI to install and manage Krateo platform deployments.

## Purpose

This repository contains standardized Krateo platform deployment configurations for different infrastructure scenarios. These manifests define the complete installation blueprint for the Krateo platform, including all core components (authentication, event management, analytics, and cost optimization services).

## Why It's Needed

Different Kubernetes environments have different networking and service exposure requirements. These configuration profiles enable consistent, repeatable platform deployments across:

- **OpenShift** clusters with native security policies
- **Cloud environments** using LoadBalancer services (GCP, AWS, Azure)
- **On-premise clusters** using Ingress or NodePort services

## Integration with krateoctl

`krateoctl` is the CLI tool that consumes these configurations to automate platform installation and upgrades. When you run `krateoctl install`, it:

1. Selects the appropriate deployment profile based on your infrastructure type
2. Applies the configuration as a `KrateoPlatformOps` resource to your cluster
3. Orchestrates the installation of all platform components in the correct sequence
4. Validates service connectivity and extracts runtime information (service IPs, ports, credentials)

For more information, see the [krateoctl documentation](https://github.com/krateoplatformops/krateoctl/tree/main/docs) and the [krateoctl repository](https://github.com/krateoplatformops/krateoctl).

## Argo CD Job Templates

> [!IMPORTANT]
> The Argo CD examples in [`gitops-examples/argocd/`](./gitops-examples/argocd/) show one way to use Argo CD to manage a Krateo installation inside the cluster.

Each manifest is a plain Kubernetes `Job` that uses the official `krateoctl` container image directly and then runs `krateoctl install apply`. The Job uses the pod's ServiceAccount credentials, so no kubeconfig Secret is needed. Updating the release version in GitOps changes the Job template and lets the controller recreate it instead of patching an immutable object.

> [!NOTE]
> These manifests are sample-only examples. If you need to personalize the Jobs for a specific set of needs, such as installing with a specific override profile, edit them to match those needs and publish them in a separate repository or in a fork of this one.

Supported install types:

- `nodeport`
- `loadbalancer`
- `ingress`

This keeps the release repository focused on versioned installation assets while leaving the Job recreation policy and RBAC wiring to GitOps.

If you need controller manifests to paste into the GitOps repository, see [`gitops-examples/`](./gitops-examples/README.md).

## Use Cases

- **Initial platform deployment** - Fresh installation to a new cluster
- **Version upgrades** - Rolling out platform updates with validated configurations
  - Pre-upgrade cleanup of deprecated components (see `pre-upgrade.yaml` for the automated cleanup job)
  - Removal of obsolete services with their persistent data (e.g., etcd volumes for sunset components)
  - Safe re-installation of components with new versions in correct dependency order
- **Multi-environment consistency** - Deploy identical platform functionality across dev, staging, and production
- **Configuration validation** - Pre-deployment configuration validation before applying to the cluster
