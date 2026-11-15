Tailscale Ansible Role
======================

Runs [tailscale](https://tailscale.com) as a Docker container on the target host and
registers it as a device in your tailnet. The device name in the tailnet is the ansible
inventory host name, and the auth key is read from a dotenv file on the ansible control
node so it never lands in the repository.

Requirements
------------

- Docker and Docker Compose v2 on the target host (pulled in via the `geerlingguy.docker`
  role dependency)
- The `community.docker` collection on the control node
- `/dev/net/tun` available on the target host, unless `tailscale_userspace: true`
- A reusable or single-use auth key from the
  [tailscale admin console](https://login.tailscale.com/admin/settings/keys)

The auth key
------------

Add the key to `.secrets/.env` on the control node (the file is gitignored):

```
TS_AUTHKEY=tskey-auth-xxxxxxxxxxxx
```

The role reads it with a `lookup('file', ...)`, so the file is only ever opened on the
control node. It is written to `{{ tailscale_compose_dir }}/.env` on the target host with
mode `0600` and is referenced from the compose file, so the key never appears in the
process list or in `docker inspect` output. Tasks touching the key set `no_log: true`.

To bypass the dotenv file entirely, pass the key directly:

```bash
ansible-playbook pb-tailscale.yml -e tailscale_authkey=tskey-auth-xxxxxxxxxxxx
```

Role Variables
--------------

See `defaults/main.yml`:

```yaml
tailscale_compose_dir: /opt/tailscale
tailscale_compose_project_name: tailscale
tailscale_image: tailscale/tailscale:latest
tailscale_container_name: tailscale
tailscale_hostname: "{{ inventory_hostname }}"
tailscale_env_file: "{{ playbook_dir }}/.secrets/.env"
tailscale_authkey: ""
tailscale_extra_args: ""
tailscale_userspace: false
```

The container runs with `network_mode: host`, `NET_ADMIN`/`NET_RAW` and the tun device, so
the tailnet interface belongs to the host and other services (for example k3s) can reach it.
Tailscale state lives in `{{ tailscale_compose_dir }}/state`, which keeps the node
registered across container recreations — after the first run the auth key is no longer
needed to come back online.

The node is reachable at its own tailnet address only. It is deliberately not a subnet
router or an exit node, since the point is to let people reach this host (and the k3s API
server on it) rather than to bridge the home LAN onto the tailnet. Should that change,
extend `tailscale_extra_args` with `--advertise-routes=...` or `--advertise-exit-node`,
approve the routes in the admin console, and enable `net.ipv4.ip_forward` on the host.

Example Playbook
----------------

```yaml
- name: Deploy tailscale container and join the tailnet
  hosts: server
  become: true
  roles:
    - role: tailscale
```

Verifying
---------

The role waits until the tailscale backend reports `Running` and prints the assigned
tailnet addresses. Manually:

```bash
ssh trpi-cm4-7 sudo docker exec tailscale tailscale status
```

License
-------

MIT-0
