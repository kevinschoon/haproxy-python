__author__ = 'kevinschoon@gmail.com'

import unittest
from haproxy.client import Templater, HAProxyConfig
from haproxy.models import BackendSection
from haproxy.exceptions import BadDeclaration

class TestTemplater(unittest.TestCase):

    def setUp(self):
        self.templater = Templater()

    def test_create(self):
        self.assertIsInstance(self.templater, Templater)

    def test_render(self):
        self.assertIsInstance(self.templater.render(), HAProxyConfig)
        self.assertIn('haproxy-python', str(self.templater.render()))

    def test_configuration(self):
        cfg = self.templater.render()
        self.assertEquals(cfg.test(), True)

class TestExamples(unittest.TestCase):

    def setUp(self):
        self.templater = Templater()

    def test_example_1(self):
        pass

    def test_example_2(self):
        service = 'backend-service-1'
        backend = BackendSection.from_defaults(name=service)
        backend.add_line('server', 'backend-server-1', '192.168.1.10:8000')
        t = Templater(backend_sections=[backend])
        self.assertIn('backend-server-1', str(t.render()))
        print(t.render())

    def test_example_3(self):
        service = 'backend-server-2'
        backend = BackendSection.from_defaults(name=service)
        with self.assertRaises(BadDeclaration):
            backend.add_line('invalid-option', 'backend-server-2', '192.168.1.11:8000')
