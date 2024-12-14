# Pillar top.sls example
"{{saltenv}}":
  '*':
    - common

  'web*':
    - webserver

