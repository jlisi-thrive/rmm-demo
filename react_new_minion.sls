{% set minionGrains = salt['grains.items']() | tojson %}
{% set defaultGateway = salt['ip.get_default_gateway']() %}

default_gateway:
  grains.present:
    - value: {{defaultGateway}}