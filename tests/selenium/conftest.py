import pytest
import os
from selenium import webdriver

browsers = {
  'firefox': webdriver.Firefox,
  'chrome': webdriver.Chrome,
}

@pytest.fixture(scope='session', params=browsers.keys())
def driver(request):
  ''' driver factory, for allowing more than one browser object in a fixture '''
  if 'DISPLAY' not in os.environ:
    pytest.skip('Test requires display server (export DISPLAY)')

  class DriverFactory(object):
    def get(self):
      b = browsers[request.param]()
      request.addfinalizer(lambda *args: b.quit())  
      return b
  return DriverFactory()

@pytest.fixture
def bf(driver, url):
  ''' browser factory, for allowing more than one browser object in a fixture '''
  class BrowserFactory(object):
    def get(self):
      b = driver.get()
      b.set_window_size(1200, 800)
      b.implicitly_wait(3)
      b.get(url)
      return b
  return BrowserFactory()

def pytest_addoption(parser):
  parser.addoption('--url', action='store',
        default='http://localhost:8111/')

@pytest.fixture(scope='session')
def url(request):
  return request.config.option.url