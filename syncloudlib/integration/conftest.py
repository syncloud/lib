import pytest
from syncloudlib.integration.installer import get_data_dir, get_app_dir, get_service_prefix

SYNCLOUD_INFO = 'syncloud.info'


def pytest_addoption(parser):
    parser.addoption("--domain", action="store")
    parser.addoption("--device-host", action="store")
    parser.addoption("--app-archive-path", action="store")
    parser.addoption("--app", action="store")


@pytest.fixture(scope='session')
def app(request):
    return request.config.getoption("--app")


@pytest.fixture(scope='session')
def app_archive_path(request):
    return request.config.getoption("--app-archive-path")


@pytest.fixture(scope='session')
def device_host(request):
    return request.config.getoption("--device-host")


@pytest.fixture(scope='session')
def domain(request):
    return request.config.getoption("--domain")


@pytest.fixture(scope='session')
def main_domain():
    return SYNCLOUD_INFO


@pytest.fixture(scope='session')
def device_domain(domain, main_domain):
    return '{0}.{1}'.format(domain, main_domain)


@pytest.fixture(scope='session')
def app_domain(app, device_domain):
    return '{0}.{1}'.format(app, device_domain)
    

@pytest.fixture(scope="session")
def platform_data_dir():
    return get_data_dir('platform')

    
@pytest.fixture(scope="session")
def data_dir(app):
    return get_data_dir(app)


@pytest.fixture(scope="session")
def app_dir(app):
    return get_app_dir(app)
    

@pytest.fixture(scope="session")
def service_prefix():
    return get_service_prefix()
