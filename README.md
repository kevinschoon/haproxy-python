# haproxy-python

This tool aims to be a general library for using HAProxy in Python.


Currently you can:
  - generate and validate HAProxy configuration files

Road Map:
  - manage the HAProxy process as a daemon
  - collect statistics via [stats socket](http://cbonte.github.io/haproxy-dconv/configuration-1.5.html#stats socket)
  - RESTful API

### Install

Source installation is only available at the moment this project will be available on PyPi soon.

```bash
$ git clone git@github.com:greencase/haproxy-python.git
$ cd haproxy-python
$ pip install .
```
### Example

The simplest possible configuration will use sane defaults and setup the "stats" listener.

```python
from haproxy.client import Templater
print(Templater().render())

>>>
"""
# This file was generated with haproxy-python

global
daemon
maxconn 4092

defaults
log global
retries 3
maxconn 2000
timeout connect 5s
timeout client 50s
timeout server 50s

listen stats
bind *:9000
mode http
stats enable
stats auth admin:admin
stats realm HAproxy\ Statistics
stats uri /
"""
```
To add new configuration you can either extend the existing `BackendSection`, `FrontendSection`, or `ListenerSection` classes or subclass the Section object.

```python

from haproxy.client import Templater
from haproxy.models import BackendSection

service = backend-service-1

backend = BackendSection.from_defaults(name=service)
backend.add_line(keyword='server', 'backend-server-1', '192.168.1.10:8000')
t = Templater(backends=[backend])
print(t.render())
>>>
"""
backend backend-service-1
mode http
option tcplog
server backend-server-1 192.168.1.10:8000
"""

```

Currently only keyword validation is possible however I hope to extend this to include parameter and ACL validation as well.

```python
from haproxy.client import Templater
from haproxy.models import Backend
from haproxy.exceptions import BadConfiguration
service = backend-service-2

backend = Backend.from_defaults(name=service)
backend.add_line(keyword='invalid-option', 'backend-server-2', '192.168.1.11:8000')

>>>
"""
Traceback (most recent call last):
...
  raise BadDeclaration(keyword)
haproxy.exceptions.BadDeclaration: invalid-option
"""

# Validate a generated configuration.
cfg = Templater().render()
try:
  cfg.test()
  print(cfg)
except BadConfiguration:
  print('Invalid HAProxy configuration!')

```
