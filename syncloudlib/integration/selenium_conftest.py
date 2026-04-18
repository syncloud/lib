import os
from os.path import join, exists

import pytest
from selenium import webdriver

from syncloudlib.integration.conftest import pytest_addoption as _base_pytest_addoption
from syncloudlib.integration.selenium_wrapper import SeleniumWrapper


def pytest_addoption(parser):
    _base_pytest_addoption(parser)
    parser.addoption("--ui-mode", action="store", default="desktop")
    parser.addoption("--browser", action="store", default="firefox")
    parser.addoption("--browser-height", action="store", default=2000)


@pytest.fixture(scope='session')
def ui_mode(request):
    return request.config.getoption("--ui-mode")


@pytest.fixture(scope='session')
def browser(request):
    return request.config.getoption("--browser")


@pytest.fixture(scope='session')
def browser_height(request):
    return int(request.config.getoption("--browser-height"))


def new_firefox_driver(hub_url, ui_mode):
    mobile_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 16_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Mobile/15E148 Safari/604.1"
    options = webdriver.FirefoxOptions()
    options.set_preference('app.update.auto', False)
    options.set_preference('app.update.enabled', False)
    if ui_mode == "mobile":
        options.set_preference("general.useragent.override", mobile_agent)
    options.set_preference("devtools.console.stdout.content", True)
    options.set_capability('acceptInsecureCerts', True)
    options.set_capability('se:recordVideo', True)
    options.set_preference("media.navigator.streams.fake", True)
    options.set_preference("media.navigator.permission.disabled", True)

    return webdriver.Remote(
        command_executor=hub_url,
        options=options
    )


def new_chrome_driver(hub_url, ui_mode):
    mobile_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 16_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Mobile/15E148 Safari/604.1"
    options = webdriver.ChromeOptions()
    if ui_mode == "mobile":
        options.add_argument('user-agent={}'.format(mobile_agent))
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
    options.set_capability('acceptInsecureCerts', True)
    options.set_capability('se:recordVideo', True)
    options.add_argument("--use-fake-ui-for-media-stream")
    options.add_argument("--use-fake-device-for-media-stream")
    return webdriver.Remote(
        command_executor=hub_url,
        options=options
    )


@pytest.fixture(scope="session")
def driver(ui_mode, browser, browser_height, request):
    hub_url = 'http://selenium:4444/wd/hub'
    width = 1024
    if ui_mode == "mobile":
        width = 400

    if browser == "firefox":
        driver = new_firefox_driver(hub_url, ui_mode)
    else:
        driver = new_chrome_driver(hub_url, ui_mode)
    driver.set_window_rect(0, 0, width, browser_height)

    def driver_quit():
        driver.quit()

    request.addfinalizer(driver_quit)

    return driver


@pytest.fixture(scope="session")
def screenshot_dir(artifact_dir, ui_mode):
    ui_dir = join(artifact_dir, ui_mode)
    if not exists(ui_dir):
        os.mkdir(ui_dir)
    screenshot_dir = join(ui_dir, 'screenshot')
    if not exists(screenshot_dir):
        os.mkdir(screenshot_dir)
    return screenshot_dir


@pytest.fixture(scope="session")
def selenium_timeout():
    return 10


@pytest.fixture(scope="session")
def selenium(driver, ui_mode, screenshot_dir, app_domain, selenium_timeout, browser):
    return SeleniumWrapper(driver, ui_mode, screenshot_dir, app_domain, selenium_timeout, browser)
