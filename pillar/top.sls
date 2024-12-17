# Pillar top.sls example
"{{saltenv}}":
  '*':
    - common

  'web*':
    - webserver

  'salt*':
    - salt

  'salt-ci*':
    - salt.identify.{{ grains.nodename }}

  'ghar*':
    - ghar
