# Pillar top.sls example
"{{saltenv}}":
  '*':
    - common

  'web*':
    - webserver

  'salt*':
    - salt

  'salt-ci*':
    - salt.identify.{{ grains.id | replace('.', '_') }}

  'ghar*':
    - ghar
