# interactions-ansible-roles

Ansible roles shared by our infrastructure repositories, packaged as the collection `interactions.roles`.
They used to live in each repository that needed them, so the copies drifted apart. Here they have one
version that every repository pins.

## Roles

| Role | What it does |
| --- | --- |
| `aiopslab` | Runs AIOpsLab experiments against a k3s or kind cluster from a Docker container |
| `krkn` | The krkn chaos engineering operator, its console and `krknctl`, with the clusters it attacks |
| `minikube_shared` | Keeps one minikube cluster of one account up and its kubeconfig current |
| `portainer` | Portainer CE in Docker Compose, optionally connected to Kubernetes |
| `syncthing` | Syncthing in a Docker container |
| `tailscale` | Tailscale in a Docker container that joins the host to the tailnet |
| `users` | Local accounts with SSH keys and a shared supplementary group |
| `vcluster` | A vcluster in a namespace of a host cluster, e.g. as a target of `krkn` |
| `zsh` | zsh with oh-my-zsh, plugins and oh-my-posh for one account |

Each role's README lists its variables.

## Use

The collection is installed from git, never from Galaxy. Pin a tag in the repository's `requirements.yml`:

```yaml
collections:
  - name: https://github.com/GiugAles/interactions-ansible-roles.git
    type: git
    version: v0.1.0
roles:
  # Not part of the collection: some roles here depend on them by name
  - name: geerlingguy.docker      # portainer, tailscale; docker for minikube_shared
  - name: andrewrothstein.minikube  # minikube and kubectl for minikube_shared
```

```shell
ansible-galaxy install -r requirements.yml
```

Then refer to a role by its full name:

```yaml
- hosts: all
  roles:
    - role: interactions.roles.minikube_shared
      minikube_shared_owner: ubuntu
```

A collection cannot install standalone roles, so the Galaxy roles that `portainer` and `tailscale` name as
dependencies have to be in the same `requirements.yml`.

## Develop

Try a change before tagging it by installing the working copy over the pinned version:

```shell
ansible-galaxy collection install --force /path/to/interactions-ansible-roles
```

Run `ansible-lint` in the root before every commit. A release is a tag `vX.Y.Z` that matches `version` in
`galaxy.yml`.

## Origin

The roles were collected on 2026-11-15 from the home infrastructure repository: `aiopslab` from the branch
`feature/aiopslab-role`, all others from `feat/asse`, which holds their newest versions.

The roles `krkn` and `vcluster` were moved on 2026-11-18 from `deploy/ansible/roles/` of
`Interactions-HSG/pitas-hs25-group10`, where PITAS ran in a vcluster that krkn attacked. Their PITAS-specific defaults
became generic: the vcluster is called `vcluster`, and the krkn console has no Ingress unless a hostname is set.

## License

MIT, see `LICENSE`. Some roles state MIT-0 in their `meta/main.yml`.
