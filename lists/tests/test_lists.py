import pytest
from django.core.urlresolvers import resolve
from django.http import HttpRequest

from lists.views import home_page


def test_root_url_resolves_to_home_page_view():
	found = resolve('/')
	assert found.func == home_page


def test_home_page_returns_correct_html():
	request = HttpRequest()
	response = home_page(request)
	assert response.content.startswith(b'<html>')
	assert b'<title>To-Do lists</title>' in response.content
	assert response.content.endswith(b'</html>')