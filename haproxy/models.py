__author__ = 'kevinschoon@gmail.com'

from haproxy.config import get_config_options
from haproxy.exceptions import BadDeclaration

class Declaration:
    """
    Declarations represent any line of text within a Section
    """

    def __init__(self, keyword, name=None):
        """
        Declarations must be given a keyword (any valid configuration key) and may be given an optional name.
        The resulting str format will be KEYWORD [name] arg..arg..arg
        :param keyword: str
        :param name: srt
        :return: None
        """
        self.keyword = keyword
        self.args = list()
        self.name = name

    def set_arguments(self, *args):
        """
        Extend the declaration's set of arguments.
        :param args: list
        :return: None
        """
        self.args.extend(args)

    def __str__(self):
        _str = self.keyword
        if self.name:
            _str += ' ' + self.name + ' '
        if self.args:
            return _str + ' ' + ' '.join(self.args)
        else:
            return _str

class ACL(Declaration):
    def __init__(self, acl_name, ):
        super().__init__(keyword='acl')

class Section:
    """
    A Section represents HAProxy's configuration sections.
    See http://cbonte.github.io/haproxy-dconv/configuration-1.5.html#2
    """
    defaults = []
    section = '*'

    def __init__(self, version='1.5', name=None, defaults=None):
        self.name = name
        self._lines = list()
        self._lines.append(Declaration(keyword=self.section, name=name))
        self.config = get_config_options(version)[self.section] if self.section != '*' else get_config_options(version)
        if self.section == '*':
            _config = list()
            for section in self.config:
                _config.extend(list(self.config[section]))
            self.config = _config
        self.config = dict((key, Declaration(keyword=key)) for key in self.config)

        if defaults:
            for default in defaults:
                self.add_line(*default)

    def add_line(self, keyword, *args):
        """
        Add a Declaration line to this section.
        :param keyword: str
        :param args: list
        :return: None
        """
        if keyword in self.config:
            _declaration = self.config[keyword]
            if _declaration in self._lines:
                _declaration = Declaration(keyword=keyword)
            _declaration.set_arguments(*args)
            self._lines.append(_declaration)
        else:
            raise BadDeclaration(keyword)

    @classmethod
    def from_defaults(cls, name=None):
        return cls(name=name, defaults=cls.defaults)


class GlobalSection(Section):
    """
    Global HAProxy section.
    See http://cbonte.github.io/haproxy-dconv/configuration-1.5.html#3
    """
    section = 'global'
    defaults = [
        ('daemon', ''),
        ('maxconn', '4092'),
        ('log', '127.0.0.1', 'local0'),
        ('log', '127.0.0.1', 'local1', 'notice')
    ]


class DefaultsSection(Section):
    section = 'defaults'
    defaults = [
        ('log', 'global'),
        ('retries', '3'),
        ('maxconn', '2000'),
        ('timeout connect', '5s'),
        ('timeout client', '50s'),
        ('timeout server', '50s')
    ]


class ListenSection(Section):
    defaults = [
        ('option httplog', ''),
        ('mode',  'http', )
    ]
    section = 'listen'


class FrontendSection(Section):
    section = 'frontend'

class BackendSection(Section):
    section = 'backend'

class StatsSection(Section):
    defaults = [
        ('bind', '*:9000'),
        ('mode',  'http', ),
        ('stats enable', ),
        ('stats auth', 'admin:admin'),
        ('stats realm', 'HAproxy\ Statistics'),
        ('stats uri', '/')
    ]
    section = 'listen'
