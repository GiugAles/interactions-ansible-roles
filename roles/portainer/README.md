Portainer Ansible Role
======================

This Ansible role deploys Portainer CE (Community Edition) using Docker Compose and optionally deploys the Portainer Agent to a Minikube cluster for Kubernetes management.

Requirements
------------

- Docker and Docker Compose installed on target hosts (handled by role dependency)
- Minikube installed and running (if deploying agent to Kubernetes)
- kubectl configured to access the Minikube cluster (for Kubernetes operations)
- Ansible collections (automatically installed when using this role):
  - `community.docker` (for Docker Compose management)
  - `kubernetes.core` (for potential future Kubernetes module usage)

Role Variables
--------------

Available variables are listed below, along with default values (see `defaults/main.yml`):

```yaml
# Portainer deployment directory
portainer_deploy_dir: "/opt/portainer"

# Docker compose settings
portainer_compose_project_name: "portainer"

# Minikube settings
portainer_deploy_to_minikube: true
```

Dependencies
------------

This role formally declares the following dependencies in `meta/main.yml`:

**Role Dependencies:**
- `geerlingguy.docker` - Ensures Docker is installed and configured

**Collection Dependencies:**
- `community.docker` - Required for Docker Compose v2 operations
- `kubernetes.core` - Available for Kubernetes module operations (currently using kubectl directly)

Features
--------

- **Docker Deployment**: Deploys Portainer CE using Docker Compose in `/opt/portainer`
- **Minikube Integration**: Optionally deploys Portainer Agent to Minikube cluster using official manifest
- **Official Manifest**: Uses `kubectl apply -f https://downloads.portainer.io/ce2-33/portainer-agent-k8s-nodeport.yaml`
- **NodePort Access**: Agent accessible via NodePort service (port 30778)
- **Simple Deployment**: No custom templates needed, uses official Portainer resources

Example Playbook
----------------

```yaml
- hosts: docker_hosts
  become: true
  roles:
    - role: portainer
      vars:
        portainer_deploy_to_minikube: true
        portainer_agent_nodeport: 30778
```

To deploy only the Docker Compose version without Minikube:

```yaml
- hosts: docker_hosts
  become: true
  roles:
    - role: portainer
      vars:
        portainer_deploy_to_minikube: false
```

Access
------

After deployment:
- **Portainer Web UI**: `http://host:9000` or `https://host:9443`
- **Minikube Agent**: `minikube service portainer-agent -n portainer` to get the URL

Initial Setup
-------------

1. Access Portainer Web UI at `http://host:9000`
2. Create admin account
3. Add Kubernetes environment using the Minikube agent endpoint
4. Use the NodePort URL (typically `http://minikube-ip:30778`) as the environment URL

License
-------

MIT-0

Author Information
------------------

Infrastructure automation role for Portainer deployment with Kubernetes integration.
