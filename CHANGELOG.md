# Changelog

## v0.2.0 (unreleased)

- `krkn` and `vcluster`, moved from pitas-hs25-group10. `vcluster_name` defaults to `vcluster`, and
  `krkn_console_ingress_enabled` to `false`

## v0.1.0 (2026-11-15)

- The roles of the home infrastructure repository: `aiopslab`, `minikube_shared`, `portainer`, `syncthing`,
  `tailscale`, `users` and `zsh`
- `minikube_shared`: `minikube_shared_start_args` passes further flags to `minikube start`
- `portainer`, `syncthing`: lint-clean; the handler is now `Restart portainer`
