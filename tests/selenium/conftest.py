import pytest
import os
from selenium import webdriver

browsers = {
  'firefox': webdriver.Firefox,
  'chrome': webdriver.Chrome,
}

@pytest.fixture(scope='session', params=browsers.keys())
def driver(request):
  if 'DISPLAY' not in os.environ:
    pytest.skip('Test requires display server (export DISPLAY)')

  b = browsers[request.param]()
  request.addfinalizer(lambda *args: b.quit())
  return b

@pytest.fixture
def b(driver, url):
  b = driver
  b.set_window_size(1200, 800)
  b.implicitly_wait(3)
  b.get(url)

  return b

def pytest_addoption(parser):
  parser.addoption('--url', action='store',
        default='http://localhost:8111/')

@pytest.fixture(scope='session')
def url(request):
  return request.config.option.url