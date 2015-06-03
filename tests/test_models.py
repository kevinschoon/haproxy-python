__author__ = 'kevinschoon@gmail.com'

import unittest

from haproxy.models import BackendSection, DefaultsSection, FrontendSection, \
    GlobalSection, ListenSection, Section, Declaration

from haproxy.exceptions import BadDeclaration

class TestDeclaration(unittest.TestCase):
    def setUp(self):
        self.declaration = Declaration(keyword='awesome')

    def test_create(self):
        self.assertIsInstance(self.declaration, Declaration)
        self.assertEquals('awesome', str(self.declaration))

    def test_add_arguments(self):
        self.declaration.set_arguments('100', '1000')
        self.assertEquals('awesome 100 1000', str(self.declaration))

class TestSection(unittest.TestCase):
    def setUp(self):
        self.section = Section(name='test_name')

    def test_create(self):
        self.assertIsInstance(self.section, Section)

    def test_add_section(self):
        self.section.add_line('monitor-uri', 'fuu', 'bar')

    def test_bad_section(self):
        with self.assertRaises(BadDeclaration):
            self.section.add_line(('NotGonnaWork', '0'))

class TestBackendSection(unittest.TestCase):
    def setUp(self):
        self.backend = BackendSection()

    def test_create(self):
        self.assertIsInstance(self.backend, BackendSection)

class TestDefaultsSection(unittest.TestCase):
    def setUp(self):
        self.defaults = DefaultsSection()

    def test_create(self):
        self.assertIsInstance(self.defaults, DefaultsSection)

class TestFrontendSection(unittest.TestCase):
    def setUp(self):
        self.frontend = FrontendSection()

    def test_create(self):
        self.assertIsInstance(self.frontend, FrontendSection)

class TestGlobalSection(unittest.TestCase):
    def setUp(self):
        self.global_section = GlobalSection()

    def test_create(self):
        self.assertIsInstance(self.global_section, GlobalSection)

class TestListenSection(unittest.TestCase):
    def setUp(self):
        self.listen = ListenSection()

    def test_create(self):
        self.assertIsInstance(self.listen, ListenSection)

class TestSectionsFromDefaults(unittest.TestCase):
    def setUp(self):
        self.global_section = GlobalSection.from_defaults()

    def test_create(self):
        self.assertIsInstance(self.global_section, GlobalSection)
        self.assertEquals(len(GlobalSection.defaults) + 1, len(self.global_section._lines))