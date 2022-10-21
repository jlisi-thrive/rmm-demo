winlogbeat:
  pkg.installed:
    - refresh: True

push_winlogbeatconfig:
  file.managed:
    - name: C:\Program Files\Winlogbeat\winlogbeat.yml
    - source: salt://winlogbeat.yml
    - force: True

winlogbeat:
  service.running:
    - enable: True