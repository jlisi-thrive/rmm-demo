salt.state:
  - tgt: {{ data.id }}
  - sls:
    - set_customgrain