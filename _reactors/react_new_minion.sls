do_first_thing:
  local.state.apply:
    - tgt: {{ data['id'] }}
    - arg:
      - set_customgrain

do_second_thing:
  local.http.query:
    - name: https://thrivedev.service-now.com/api/thn/salt/minion
    - method: POST
    - status: 200
    - header_dict:
        Accept: application/json
        Content-Type: application/json
    - data: ''