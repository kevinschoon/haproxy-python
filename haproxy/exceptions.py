__author__ = 'kevinschoon@gmail.com'

class HAProxyException(Exception):
    pass

class BadDeclaration(HAProxyException):
    pass

class BadConfiguration(HAProxyException):
    pass
