__author__ = 'kevinschoon@gmail.com'

from setuptools import setup, find_packages

setup(
    name='haproxy-python',
    version='0.0.1',
    packages=find_packages(),
    package_dir={'haproxy': 'haproxy'},
    include_package_data=True,
    install_requires=['jinja2'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4'
    ]
)
