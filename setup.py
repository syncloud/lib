from setuptools import setup
from os.path import join, dirname

requirements = [
    'jsonpickle==0.7.1',
    'requests==2.11.1',
    'Jinja2==2.9.6',
    'requests-unixsocket==0.1.5'
]

version = open(join(dirname(__file__), 'version')).read().strip()

setup(
    name='syncloud-lib',
    version=version,
    install_requires = requirements,
    description='Syncloud common library',
    packages=['syncloud_app', 'syncloudlib', 'syncloudlib.integration', 'syncloudlib.application'],
    py_modules = ['convertible'],
    license='GPLv3',
    author='Syncloud',
    author_email='syncloud@syncloud.it',
    url='https://github.com/syncloud/lib')