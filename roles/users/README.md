# users

Creates local user accounts and joins them to a shared supplementary group.

## Role Variables

| Variable | Default | Description |
| --- | --- | --- |
| `users_list` | `[]` | Accounts to manage. See below. |
| `users_group` | `""` | Supplementary group every account joins. Empty disables it. |
| `users_default_shell` | `""` | Shell for accounts without an explicit `shell`. Empty leaves the shell unmanaged, so a later role (such as `zsh`) can own it without the two fighting. |
| `users_create_home` | `true` | Create home directories. |

Each entry of `users_list` needs a `name`. Optional keys: `comment`, `uid`,
`shell`, `groups` (further supplementary groups) and `ssh_keys` (public keys
authorised for the account).

Accounts are created with a locked password, so an entry without `ssh_keys` has
no way to log in.

## Example

```yaml
- hosts: all
  become: true
  roles:
    - role: users
      users_group: evomas
      users_list:
        - name: alessandro
          ssh_keys:
            - "ssh-ed25519 AAAA... alessandro"
        - name: svenja
```

## License

MIT-0
