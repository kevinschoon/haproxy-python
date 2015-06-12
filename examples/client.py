"""
Example of using haproxy-python and Marathon to generate a configuration for service discovery.
"""

__author__ = 'kevinschoon@gmail.com'

import requests

from haproxy.client import Templater
from haproxy.models import ListenSection, FrontendSection, BackendSection

def _get_tasks(server):
    config = dict()
    tasks = requests.get(url=server + '/v2/tasks')
    for line in tasks.text.split('\n'):
        try:
            _t = line.split('\t')
            app = _t[0]
            port = _t[1]
            config[app] = dict()
            config[app]['port'] = port
            config[app]['servers'] = list()
            for server in _t[2:]:
                if server:
                    _server = server.split(':')
                    host = _server[0]
                    port = _server[1]
                    config[app]['servers'].append((host, port))
        except IndexError:
            pass

    return config

def run(server):
    config = _get_tasks(server)
    sections = list()
    for app in config:
        section = ListenSection.from_defaults(name=app)
        section.add_line('bind', '0.0.0.0:{}'.format(config[app]['port']))
        for server in config[app]['servers']:
            section.add_line('server', app, '{}:{}'.format(server[0], server[1]))
        sections.append(section)

    t = Templater(use_stats=True, listen_sections=sections)
    cfg = t.render()
    cfg.test()
    print(cfg)


if __name__ == '__main__':
    marathon_server = 'http://ubuntu:8080'
    run(marathon_server)
