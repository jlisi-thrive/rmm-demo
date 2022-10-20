do_first_thing:
  local.state.apply:
    - tgt: {{ data['id'] }}
    - arg:
      - set_customgrain

do_winlogbeat_install:
  local.state.apply:
    - tgt: {{ data['id'] }}
    - arg:
      - install_winlogbeat

{# do_second_thing:
  local.state.apply:
    - tgt: {{ data['id'] }}
    - arg:
      - send_customhttp #}