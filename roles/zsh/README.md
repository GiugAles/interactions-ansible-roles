# Zsh Role

This Ansible role installs and configures zsh with oh-my-zsh and optionally oh-my-posh, and sets zsh as the default shell for a specified user.

## Requirements

- Ansible 2.9 or higher
- Target system should have internet connectivity for downloading oh-my-zsh and oh-my-posh
- Sudo privileges on the target system

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

### Basic Configuration

```yaml
# User to configure zsh for
zsh_user: "{{ ansible_user | default('root') }}"

# User's home directory
zsh_user_home: "{{ ansible_user_dir | default('/home/' + zsh_user) }}"
```

### Oh-My-Zsh Configuration

```yaml
# Oh-My-Zsh theme
zsh_ohmyzsh_theme: "robbyrussell"

# Oh-My-Zsh plugins to enable
zsh_ohmyzsh_plugins:
  - git
  - sudo
  - history
  - colored-man-pages
```

### Oh-My-Posh Configuration

```yaml
# Enable oh-my-posh (overrides oh-my-zsh theme)
zsh_enable_ohmyposh: false

# Oh-My-Posh theme to use
zsh_ohmyposh_theme: "jandedobbeleer"
```

### Font Configuration

```yaml
# Install Nerd Fonts using oh-my-posh CLI (recommended for oh-my-posh themes)
zsh_install_fonts: true
```

### Plugin Configuration

```yaml
# Whether to install additional zsh plugins
zsh_install_plugins: true

# Additional zsh plugins to install
zsh_plugins:
  - name: "zsh-autosuggestions"
    repo: "https://github.com/zsh-users/zsh-autosuggestions"
  - name: "zsh-syntax-highlighting"
    repo: "https://github.com/zsh-users/zsh-syntax-highlighting.git"
```

### Custom Configuration

```yaml
# Aliases placed right below the example aliases in .zshrc
zsh_aliases: ""

# Custom configuration to append to .zshrc
zsh_custom_config: |
  # Add your custom configuration here
```

## Dependencies

None.

## Example Playbook

### Basic Usage

```yaml
- hosts: servers
  roles:
    - role: zsh
      zsh_user: "myuser"
```

### Advanced Configuration

```yaml
- hosts: servers
  roles:
    - role: zsh
      zsh_user: "developer"
      zsh_ohmyzsh_theme: "agnoster"
      zsh_enable_ohmyposh: true
      zsh_ohmyposh_theme: "paradox"
      zsh_ohmyzsh_plugins:
        - git
        - sudo
        - docker
        - kubectl
        - history
        - colored-man-pages
      zsh_custom_config: |
        # Custom aliases
        alias ll='ls -alF'
        alias la='ls -A'
        alias l='ls -CF'
        
        # Custom exports
        export EDITOR=vim
```

## What This Role Does

1. **Installs required packages**: zsh, git, curl, and unzip
2. **Installs oh-my-zsh**: Downloads and installs oh-my-zsh framework
3. **Installs oh-my-posh** (optional): Uses official installation script from ohmyposh.dev
4. **Installs Nerd Fonts** (optional): Uses oh-my-posh CLI to install MesloLGM NF fonts
5. **Configures .zshrc**: Creates a customized .zshrc file with specified themes and plugins
6. **Sets default shell**: Changes the user's default shell to zsh
7. **Installs additional plugins**: Installs popular zsh plugins like autosuggestions and syntax highlighting

## Supported Platforms

- Ubuntu (all versions)
- Debian (all versions)
- RHEL/CentOS/Rocky Linux (all versions)
- Fedora (all versions)

## Architecture Support

The role automatically detects the system architecture and downloads the appropriate oh-my-posh binary:
- x86_64 (amd64)
- aarch64 (arm64) 
- armv7l (arm)

## Notes

- The role will backup the existing `.zshrc` file if it exists
- After running this role, users need to log out and log back in for the shell change to take effect
- **Uses official installation methods**: oh-my-posh via `curl -s https://ohmyposh.dev/install.sh` and fonts via `oh-my-posh font install meslo`
- Oh-my-posh is installed to `~/.local/bin/oh-my-posh` and added to PATH
- Nerd Fonts are installed using the oh-my-posh CLI for optimal compatibility
- Additional plugins are installed to `~/.oh-my-zsh/custom/plugins/`

## License

MIT-0

## Author Information

This role was created for Ansible infrastructure management.