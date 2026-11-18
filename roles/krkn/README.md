# krkn

Installs the [krkn](https://krkn-chaos.dev) chaos engineering operator with Helm, optionally its web console and
the CLI `krknctl`, and registers the clusters that krkn attacks. It can remove all of this again.

The krkn operator never runs scenarios against the cluster it is installed in. To attack an application on the same
machine, run the application in a vcluster (see the `vcluster` role) and register that as a target.

Repeated runs report no change: the role only runs `helm upgrade` when the release differs from what it would
install, and passes the console's JWT key back in, which the chart would otherwise regenerate on every upgrade.

## Role Variables

| Variable | Default | Description |
| --- | --- | --- |
| `krkn_state` | `present` | `present` installs, `absent` removes. Read from the environment variable `KRKN_STATE` if set, which also accepts `install` and `uninstall` |
| `krkn_release_name` | `krkn-operator` | Helm release of the operator |
| `krkn_namespace` | `krkn-operator-system` | Namespace of the operator |
| `krkn_chart_ref` | `oci://quay.io/krkn-chaos/charts/krkn-operator` | Chart of the operator |
| `krkn_chart_version` | `1.0.0` | Version of the chart |
| `krkn_wait_timeout` | `10m` | How long Helm waits |
| `krkn_kubeconfig` | `""` | Kubeconfig on the target host. Empty uses `$KUBECONFIG` or `~/.kube/config` |
| `krkn_console_enabled` | `true` | Deploy the web console. Without an Ingress, reach it with `kubectl -n krkn-operator-system port-forward svc/krkn-operator-console 3000:3000` |
| `krkn_console_ingress_enabled` | `false` | Publish the console at `krkn_console_hostname`. Its first visitor creates the admin user, so create it right after the install |
| `krkn_console_hostname` | `""` | Hostname of the console. Required with the Ingress |
| `krkn_console_ingress_class_name` | `""` | IngressClass of the console. Empty uses the cluster's default |
| `krkn_console_tls_enabled` | `true` | Request a certificate for the console's Ingress |
| `krkn_console_tls_cluster_issuer` | `letsencrypt` | cert-manager ClusterIssuer for that certificate. It has to exist |
| `krkn_extra_values` | `{}` | Helm values merged into the role's |
| `krkn_targets` | `[]` | Clusters to attack: each a `name` and a `kubeconfig` (string) whose server the operator's pods reach. Registered by `tasks_from: targets` |
| `krkn_remove_crds` | `true` | Remove the operator's CRDs on uninstall. Helm never does |
| `krkn_remove_namespace` | `true` | Remove `krkn_namespace` on uninstall. `default` and the `kube-*` namespaces are never removed |
| `krkn_krknctl_enabled` | `true` | Install `krknctl` on the target host, and remove it on uninstall |
| `krkn_krknctl_version` | `v0.14.2-beta` | Release of [krknctl](https://github.com/krkn-chaos/krknctl/releases) |
| `krkn_krknctl_install_dir` | `~/.local/bin` | Directory of `krknctl`. Needs no sudo |

## Requirements

- `helm` and `kubectl` on the target host, with access to the cluster
- The collection `kubernetes.core`
- For `krknctl` to run scenarios: podman or docker on the target host

## Example

krkn on the host cluster, attacking an application in a vcluster:

```yaml
- hosts: k8s
  tasks:
    - name: Create the vcluster of the application
      ansible.builtin.import_role:
        name: interactions.roles.vcluster
      vars:
        vcluster_name: app

    - name: Install krkn
      ansible.builtin.import_role:
        name: interactions.roles.krkn

    - name: Register the vcluster as target of krkn
      ansible.builtin.import_role:
        name: interactions.roles.krkn
        tasks_from: targets
      vars:
        krkn_targets:
          - name: app
            kubeconfig: "{{ vcluster_kubeconfig }}"
```

Remove krkn again with `KRKN_STATE=uninstall ansible-playbook ...`, and leave out the vcluster then: it isn't
part of krkn.

## License

MIT
