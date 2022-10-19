do_first_thing:
  local.state.apply:
    - tgt: {{ data['id'] }}
    - arg:
      - set_customgrain