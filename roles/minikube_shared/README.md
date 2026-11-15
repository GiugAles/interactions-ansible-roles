# minikube_shared

Keeps a single minikube cluster, owned by one account, up and reachable.

The cluster is started only when it is down, and the owner's kubeconfig is
resynced on every run -- docker remaps the cluster's port whenever its container
is recreated (a host reboot, for instance), which silently breaks the cached
config even though `minikube status` still reports the cluster as up.

Everybody who needs the cluster shares the owner's account (the evomas accounts
can ssh in as it), so the role never writes into another account's home
directory. Nothing here needs root either: every task runs as the owner, by
sudo-ing to it or -- with `minikube_shared_become: false` -- because the
connection already is that account, which needs no privilege at all.

## Role Variables

| Variable | Default | Description |
| --- | --- | --- |
| `minikube_shared_owner` | `""` | The account that runs the cluster. Required. |
| `minikube_shared_driver` | `docker` | Driver passed to `minikube start`. |
| `minikube_shared_start_args` | `[]` | Further flags for `minikube start`, e.g. `["--cpus=max", "--memory=max"]`. Most apply only when the cluster is created. |
| `minikube_shared_become` | `true` | Sudo to the owner. Set to false when the connection already is that account, which leaves the role needing no privilege at all. |

## Requirements

- `minikube` and `kubectl` on the hosts' PATH (see `andrewrothstein.minikube`).
- The owner can use docker.
- With `minikube_shared_become: true`, `acl` is installed so ansible can become
  an unprivileged account.

## Example

```yaml
- hosts: evomas
  become: true
  roles:
    - role: interactions.roles.minikube_shared
      minikube_shared_owner: ubuntu
```

## License

MIT-0
