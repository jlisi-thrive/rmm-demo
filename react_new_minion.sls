{% set minionGrains = salt['grains.items']() | tojson %}
{% set defaultGateway = salt['ip.get_default_gateway']() %}

default_gateway:
  grains.present:
    - value: {{defaultGateway}}

{# snow_event:
  http.query:
    - name: https://thrivedev.service-now.com/api/thn/salt/minion
    - method: POST
    - status: 200
    - header_dict:
        Accept: application/json
        Content-Type: application/json
    - data: '{{minionGrains}}' #}