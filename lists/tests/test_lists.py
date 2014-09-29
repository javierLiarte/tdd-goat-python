import pytest
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import Item


def test_root_url_resolves_to_home_page_view():
  found = resolve('/')
  assert found.func == home_page


def test_home_page_returns_correct_html():
  request = HttpRequest()
  response = home_page(request)
  expected_html = render_to_string('home.html')
  assert response.content.decode() == expected_html


@pytest.mark.django_db
def test_home_page_can_save_a_POST_request():
  request = HttpRequest()
  request.method = 'POST'
  request.POST['item_text'] = 'A new list item'

  response = home_page(request)

  assert Item.objects.count() == 1
  new_item = Item.objects.first()
  assert new_item.text == 'A new list item'

@pytest.mark.django_db
def test_home_page_redirects_after_POST():
  request = HttpRequest()
  request.method = 'POST'
  request.POST['item_text'] = 'A new list item'

  response = home_page(request)

  assert response.status_code == 302
  assert response['location'] == '/'


@pytest.mark.django_db
def test_home_page_only_saves_items_when_necessary():
  request = HttpRequest()
  home_page(request)
  assert Item.objects.count() == 0
