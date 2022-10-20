# Software Definition File for Elasticsearch Winlogbeat

# Uses the following associated scripts
# - install.cmd
# - install.ps1
# - remove.cmd

{% set versions = ['8.4.3'] %}

winlogbeat:
  '{{ version }}':
    full_name: 'Winlogbeat'
    installer: 'salt://install.cmd'
    install_flags: {{ version }}
    uninstaller: 'salt://remove.cmd'
    cache_dir: True
