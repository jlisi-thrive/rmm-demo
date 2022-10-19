do_second_thing:
  salt.state:
    - tgt: '*'
    - sls:
      - top.sls