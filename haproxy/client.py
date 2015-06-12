__author__ = 'kevinschoon@gmail.com'

import subprocess
import uuid
import os

import jinja2

from haproxy.models import Section, GlobalSection, DefaultsSection, StatsSection
from haproxy.exceptions import BadConfiguration

class HAProxyConfig:
    """
    HAProxyConfig represents an HAProxy configuration file but with special features!
    """
    def __init__(self, config, raise_on_error=True):
        self.config = config
        self.raise_on_error = raise_on_error
        self.path = '/tmp/haproxy-test-{}'.format(str(uuid.uuid4()))  # Configurations are written to a temporary path.

    def test(self):
        """
        Test the configuration by launching the HAProxy executable with -c -f parameters
        """
        with open(self.path, 'w') as fp:
            fp.write(self.config)
        proc = subprocess.Popen(['haproxy', '-c', '-f', self.path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out = proc.communicate()
        os.remove(self.path)
        if proc.returncode == 0:
            return True
        else:
            if self.raise_on_error:
                raise BadConfiguration("{}\n{}".format(out[0], out[1]))
            else:
                return False

    def __str__(self):
        return self.config

    def __len__(self):
        return len(self.config)

class Templater:
    """
    The Templater generates an HAProxy configuration as a string and returns the HAProxyConfig object.
    """

    _base_template = """
# This file was generated with haproxy-python
{% for section in sections -%}
{% for line in section._lines -%}
    {{ line }}
{% endfor %}
{% endfor %}
    """  # TODO: Move somewhere else.

    def __init__(self, use_stats=True, global_section=None, defaults_section=None,
                 listen_sections=None, frontend_sections=None, backend_sections=None):

        self.context = dict(sections=list())

        sections = self.context['sections']

        sections.append(global_section if global_section else GlobalSection.from_defaults())
        sections.append(defaults_section if defaults_section else DefaultsSection.from_defaults())

        if use_stats:
            sections.append(StatsSection.from_defaults(name='stats'))

        if listen_sections:
            sections.extend(listen_sections)
        if frontend_sections:
            sections.extend(frontend_sections)
        if backend_sections:
            sections.extend(backend_sections)

        self.template = jinja2.Template(self._base_template)

    def render(self):
        return HAProxyConfig(self.template.render(**self.context))
