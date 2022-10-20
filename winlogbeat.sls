# Software Definition File for Elasticsearch Winlogbeat

# Uses the following associated scripts
# - install.cmd
# - install.ps1
# - remove.cmd

winlogbeat:
  '7.12.1':
    full_name: 'Winlogbeat'
    installer: 'salt://install.cmd'
    install_flags: "7.12.1"
    uninstaller: 'salt://remove.cmd'
    cache_dir: True
