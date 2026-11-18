# vcluster

Creates a [vcluster](https://www.vcluster.com) in a namespace of a host cluster, with the vcluster Helm chart.

The vcluster's API is reachable in two ways: from the pods of the host cluster as
`https://<vcluster_name>.<vcluster_namespace>.svc`, and from the target host through a node port. The role provides a
kubeconfig for each. The host cluster's ingress controller serves the vcluster's Ingresses, because the role syncs
them to the host.

The role also installs the vcluster CLI, unless one of `vcluster_version` is on the PATH already. It doesn't need the
CLI itself, but people working with the vcluster do.

## Role Variables

| Variable | Default | Description |
| --- | --- | --- |
| `vcluster_name` | `vcluster` | Name of the vcluster and of its Helm release |
| `vcluster_namespace` | `vcluster-{{ vcluster_name }}` | Namespace of the host cluster the vcluster runs in |
| `vcluster_version` | `0.34.0` | Version of the chart and of the CLI. Another version upgrades both |
| `vcluster_chart_repo_url` | `https://charts.loft.sh` | Helm repository of the chart |
| `vcluster_wait_timeout` | `10m` | How long Helm waits for the vcluster |
| `vcluster_host_kubeconfig` | `""` | Kubeconfig of the host cluster on the target host. Empty uses `$KUBECONFIG` or `~/.kube/config` |
| `vcluster_api_node_port` | `32443` | Node port of the vcluster's API, for the target host |
| `vcluster_node_address` | `""` | Address under which the target host reaches the node port. Empty uses the InternalIP of the first node |
| `vcluster_kubeconfig_path` | `~/.kube/vcluster-{{ vcluster_name }}.yaml` | Where the kubeconfig for the target host is written |
| `vcluster_extra_values` | `{}` | Helm values merged into the role's, see [vcluster.yaml](https://www.vcluster.com/docs/vcluster/configure/vcluster-yaml/) |
| `vcluster_cli_install_dir` | `~/.local/bin` | Directory of the CLI. Needs no sudo |

After a run, the fact `vcluster_kubeconfig` holds the kubeconfig whose server is the in-cluster Service, e.g. for
`krkn_targets` of the `krkn` role.

## Requirements

- `helm` and `kubectl` on the target host, with access to the host cluster
- The collection `kubernetes.core`

## Example

```yaml
- hosts: k8s
  roles:
    - role: interactions.roles.vcluster
      vcluster_name: app
```

## License

MIT
