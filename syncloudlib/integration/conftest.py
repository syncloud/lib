import logging
import os
import platform
from os.path import join, exists

import pytest

from syncloudlib.integration.device import Device
from syncloudlib.integration.installer import get_data_dir, get_app_dir, get_service_prefix, get_ssh_env_vars, \
    get_snap_data_dir

log = logging.getLogger()

arch_go_to_debian={
    "amd64": "amd64",
    "arm": "armhf",
    "arm64": "arm64",
}

arch_cpu_to_go={
    "aarch64": "arm64",
    "armv7l": "arm",
    "x86_64": "amd64",
}

def pytest_addoption(parser):
    parser.addoption("--domain", action="store")
    parser.addoption("--device-host", action="store")
    parser.addoption("--app-archive-path", action="store")
    parser.addoption("--app", action="store")
    parser.addoption("--device-user", action="store", default="user")
    parser.addoption("--build-number", action="store", default="local")
    parser.addoption("--redirect-user", action="store", default="redirect-user-notset")
    parser.addoption("--redirect-password", action="store", default="redirect-password-notset")
    parser.addoption("--distro", action="store", default="distro")
    parser.addoption("--arch", action="store")
    parser.addoption("--ver", action="store")


@pytest.fixture(scope='session')
def build_number(request):
    return request.config.getoption("--build-number")


@pytest.fixture(scope='session')
def device_user(request):
    return request.config.getoption("--device-user")


@pytest.fixture(scope='session')
def device_password():
    return 'Password1'


@pytest.fixture(scope='session')
def redirect_user(request):
    return request.config.getoption("--redirect-user")


@pytest.fixture(scope='session')
def redirect_password(request):
    return request.config.getoption("--redirect-password")


@pytest.fixture(scope='session')
def app(request):
    return request.config.getoption("--app")


@pytest.fixture(scope='session')
def version(request):
    return request.config.getoption("--ver")


@pytest.fixture(scope='session')
def app_archive_path(request, app, version, arch):
    debian_arch=arch_go_to_debian[arch]
    archive_path = request.config.getoption("--app-archive-path")
    if archive_path:
        return archive_path
    archive_path = f'{app}_{version}_{debian_arch}.snap'
    if exists(archive_path):
        log.info(f'found app archive: {archive_path}')
        return archive_path
    archive_path = f'../{archive_path}'
    if exists(archive_path):
        log.info(f'found app archive: {archive_path}')
        return archive_path
    raise Exception(f'app archive not found: {archive_path}')


@pytest.fixture(scope='session')
def device_host(request, app, domain):
    device_host = request.config.getoption("--device-host")
    if device_host:
        return device_host
    return '{0}.{1}'.format(app, domain)


@pytest.fixture(scope='session')
def domain(request, distro):
    domain = request.config.getoption("--domain")
    if domain:
        return domain
    return '{0}.com'.format(distro)


@pytest.fixture(scope='session')
def distro(request):
    return request.config.getoption("--distro")


@pytest.fixture(scope='session')
def arch(request):
    arch = request.config.getoption("--arch")
    if arch:
        return arch
    return arch_cpu_to_go[platform.machine()]


@pytest.fixture(scope='session')
def app_domain(app, domain):
    return '{0}.{1}'.format(app, domain)


@pytest.fixture(scope="session")
def platform_data_dir():
    return get_data_dir('platform')


@pytest.fixture(scope="session")
def data_dir(app):
    return get_data_dir(app)


@pytest.fixture(scope="session")
def snap_data_dir(app):
    return get_snap_data_dir(app)


@pytest.fixture(scope="session")
def app_dir(app):
    return get_app_dir(app)


@pytest.fixture(scope="session")
def service_prefix():
    return get_service_prefix()


@pytest.fixture(scope="session")
def ssh_env_vars(app):
    return get_ssh_env_vars(app)


@pytest.fixture(scope='function')
def device_session(device):
    return device.login()


@pytest.fixture(scope="session")
def device(domain, device_user,
           device_password, redirect_user, redirect_password, ssh_env_vars):
    return Device(domain, device_user,
                  device_password, redirect_user, redirect_password, ssh_env_vars)


@pytest.fixture(scope="session")
def log_dir(project_dir):
    log_dir = join(project_dir, 'log')
    if not exists(log_dir):
        os.mkdir(log_dir)
    return log_dir


@pytest.fixture(scope="session")
def artifact_dir(project_dir, distro):
    artifact_dir = join(project_dir, 'artifact', distro)
    if not exists(artifact_dir):
        os.mkdir(artifact_dir)
    return artifact_dir
