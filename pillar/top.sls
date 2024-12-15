# Pillar top.sls example
"{{saltenv}}":
  '*':
    - common

  'web*':
    - webserver

  'salt*':
    - salt

  'ghar*':
    - ghar
