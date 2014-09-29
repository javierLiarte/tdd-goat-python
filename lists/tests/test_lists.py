import pytest
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page


def test_root_url_resolves_to_home_page_view():
	found = resolve('/')
	assert found.func == home_page


def test_home_page_returns_correct_html():
	request = HttpRequest()
	response = home_page(request)
	expected_html = render_to_string('home.html')
	assert response.content.decode() == expected_html


def test_home_page_can_save_a_POST_request():
	request = HttpRequest()
	request.method = 'POST'
	request.POST['item_text'] = 'A new list item'

	response = home_page(request)

	assert 'A new list item' in response.content.decode()
	expected_html = render_to_string(
		'home.html',
		{'new_item_text': 'A new list item'}
	)
	assert response.content.decode() == expected_html