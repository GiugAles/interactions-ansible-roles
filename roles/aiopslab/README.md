AIOpsLab Ansible Role
======================

Runs [AIOpsLab](https://github.com/microsoft/AIOpsLab/) experiments from a Docker container
on `antillean`, against either the real Turing Pi k3s cluster or a local
[kind](https://kind.sigs.k8s.io/) cluster created on `antillean` itself. AIOpsLab has no
scriptable CLI, so the image bundles a small wrapper
(`files/docker/run_experiment.py`) that runs one experiment end-to-end and exits, modeled on
AIOpsLab's own `clients/gpt.py` example agent.

Everything AIOpsLab needs (Python 3.11, Poetry, the AIOpsLab checkout itself, kubectl, helm)
lives inside the container, not on `antillean` - this keeps `antillean`'s own Python
environment untouched (it's already managed with `uv` for this Ansible project) and makes
the whole thing atomically removable.

Requirements
------------

- Docker on `antillean` (pulled in via `site.yml`'s `geerlingguy.docker` role)
- The `community.docker` collection on the control node
- For the `k3s` target: the k3s cluster from `pb-k3s-control-plane.yml` must already exist
  and be reachable, with `kubectl` on `antillean` (from that same playbook's
  `andrewrothstein.kubectl` role) - the role builds its own dedicated kubeconfig by fetching
  `/etc/rancher/k3s/k3s.yaml` straight from the k3s server node, so it doesn't matter what's
  in (or missing from) `antillean`'s own `~/.kube/config`
- For the `kind` target: nothing extra - the role installs the `kind` CLI on `antillean`
  itself and creates the cluster
- An LLM API key for whichever agent you run an experiment with (see "Secrets" below)

Usage
-----

```bash
# Provision the container (and, for kind, the local cluster) without running anything yet
AIOPSLAB_STATE=present uv run ansible-playbook -i inventory/home/hosts.ini pb-aiopslab.yml \
  -e aiopslab_target=k3s   # or kind

# Also run one experiment (a real problem ID from AIOpsLab's
# aiopslab/orchestrator/problems/registry.py)
AIOPSLAB_STATE=present uv run ansible-playbook -i inventory/home/hosts.ini pb-aiopslab.yml \
  -e aiopslab_target=k3s -e aiopslab_problem_id=k8s_target_port-misconfig-detection-1

# Tear it back down - must use the same aiopslab_target used to install it
AIOPSLAB_STATE=absent uv run ansible-playbook -i inventory/home/hosts.ini pb-aiopslab.yml \
  -e aiopslab_target=k3s
```

Role Variables
--------------

See `defaults/main.yml` for the full list and their defaults. The ones you're likely to
override: `aiopslab_target` (`k3s`/`kind`), `aiopslab_problem_id`, `aiopslab_agent` (one of
the keys in AIOpsLab's `clients/registry.py`: `gpt`, `qwen`, `deepseek`, `vllm`,
`openrouter`, `generic`), `aiopslab_max_steps`, and `aiopslab_version` (a git ref - bumping
it and re-running rebuilds the image).

How the two targets differ
---------------------------

- **`k3s`**: the role fetches `/etc/rancher/k3s/k3s.yaml` directly from the k3s server node
  (`groups['server'][0]`), rewrites its server address (k3s.yaml defaults to
  `127.0.0.1:6443`, only valid on the server itself, to that node's `ansible_host`), and
  writes the result to its own dedicated kubeconfig - it never reads or writes `antillean`'s
  own `~/.kube/config`, which may be stale, point at something else entirely, or not exist.
  Chaos Mesh's default containerd socket path (`/run/containerd/containerd.sock`) doesn't
  exist on k3s (which uses `/run/k3s/containerd/containerd.sock`), so this role also
  pre-installs Chaos Mesh itself with the corrected path directly against the cluster -
  without this, AIOpsLab's own runtime auto-install of Chaos Mesh at first fault injection
  would silently fail.
- **`kind`**: the role installs the `kind` CLI on `antillean` and creates the cluster there
  (using AIOpsLab's own `kind-config-arm.yaml`, vendored into `files/`, which pulls a
  pre-built `jacksonarthurclark/aiopslab-kind-arm` node image with the target apps' ARM
  images baked in) - **not** inside the container, so `kind`'s Docker-in-Docker networking
  quirks don't need to be worked around at cluster-creation time. The container still needs
  `/var/run/docker.sock` mounted and runs with `network_mode: host`, though: AIOpsLab's own
  `Shell.exec()` shells out to `docker exec kind-control-plane ...` at runtime whenever
  `k8s_host: kind`, and kind's kubeconfig points at `127.0.0.1:<port>`, which only resolves
  correctly when the container shares `antillean`'s network namespace. Chaos Mesh isn't
  pre-installed for this target - kind nodes' containerd is already at the path AIOpsLab
  expects by default.

Both targets get their own dedicated container (`aiopslab-k3s` / `aiopslab-kind`) and state
directory (`~{{ kube_user }}/aiopslab-k3s` / `~{{ kube_user }}/aiopslab-kind`), so they can
coexist.

Secrets
-------

The bundled agents call a real LLM API. `pb-aiopslab.yml` loads
`inventory/home/group_vars/vault.yml` (ansible-vault encrypted) and exposes it as
`vault_aiopslab_openai_api_key`, which `aiopslab_llm_api_key` defaults to. Edit the real key
in with:

```bash
uv run ansible-vault edit inventory/home/group_vars/vault.yml \
  --vault-password-file .secrets/vault_pass.txt
```

The key is injected only into the one-shot `docker exec` that runs the experiment (via
`no_log: true`), never into the container's persistent environment or `docker inspect`
output. To use a different agent's key, either edit `run_experiment.py`'s environment (see
`tasks/install.yml`) or pass it directly: `-e aiopslab_llm_api_key=...`.

Scope boundary
--------------

Uninstall removes the container, and for `kind` the cluster and its dedicated
config/kubeconfig files, and for `k3s` the `chaos-mesh` Helm release, namespace and CRDs. It
deliberately does **not** remove: the built `aiopslab` image (cheap to keep for the next
install), the `kind`/`docker`/`helm` binaries or packages (shared system tooling), or
anything under `aiopslab_results_dir` (fetched experiment results - your data, not the
tool's).

Example Playbook
-----------------

```yaml
- name: Install or remove AIOpsLab on antillean
  hosts: antillean
  gather_facts: false
  vars_files:
    - inventory/home/group_vars/vault.yml
  roles:
    - aiopslab
```

License
-------

MIT-0
