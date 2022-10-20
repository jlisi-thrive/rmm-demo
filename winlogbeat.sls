# Software Definition File for Elasticsearch Winlogbeat

# Uses the following associated scripts
# - install.cmd
# - install.ps1
# - remove.cmd

{% set versions = ['7.12.1', '7.12.0',
                   '7.11.2', '7.11.1', '7.11.0',
                   '7.10.2', '7.10.1', '7.10.0',
                   '7.9.3', '7.9.2', '7.9.1', '7.9.0',
                   '7.8.1', '7.8.0',
                   '7.7.1', '7.7.0',
                   '7.6.2', '7.6.1', '7.6.0',
                   '7.5.2', '7.5.1', '7.5.0',
                   '7.4.2', '7.4.1', '7.4.0',
                   '7.3.2', '7.3.1', '7.3.0',
                   '7.2.1', '7.2.0',
                   '7.1.1',
                   '6.8.2', '6.8.1', '6.8.0'] %}

winlogbeat:
  '7.12.1':
    full_name: 'Winlogbeat'
    installer: 'salt://install.cmd'
    install_flags: "7.12.1"
    uninstaller: 'salt://remove.cmd'
    cache_dir: True
