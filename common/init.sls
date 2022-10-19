{% set defaultGateway = salt['ip.get_default_gateway']() %}
{% set minionGrains = salt['grains.items']() | tojson %}
{% set telegrafMissing = salt['service.missing']('telegraf') %}

default_gateway:
  grains.present:
    - value: {{defaultGateway}}