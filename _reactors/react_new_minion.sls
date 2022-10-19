do_first_thing:
  salt.state:
    - tgt: {{ data['id'] }}
    - sls:
      - set_customgrain