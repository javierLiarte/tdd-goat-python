import pytest
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import Item, List

testserver_url = 'http://testserver'

def test_root_url_resolves_to_home_page_view():
  found = resolve('/')
  assert found.func == home_page

@pytest.mark.django_db
def test_home_page_returns_correct_html():
  request = HttpRequest()
  response = home_page(request)
  expected_html = render_to_string('home.html')
  assert response.content.decode() == expected_html


class TestListView(object):

  @pytest.mark.django_db
  def test_uses_list_template(self, client):
    response = client.get('/lists/the-only-list-in-the-world/')
    template_names = [t.name for t in response.templates]
    assert 'list.html' in template_names

  @pytest.mark.django_db
  def test_list_view_displays_all_list_items(self, client):
    list_ = List.objects.create()
    Item.objects.create(text='itemey 1', list=list_)
    Item.objects.create(text='itemey 2', list=list_)

    response = client.get('/lists/the-only-list-in-the-world/')

    assert 'itemey 1' in response.content.decode()
    assert 'itemey 2' in response.content.decode()

class TestNewList(object):

  @pytest.mark.django_db
  def test_saving_a_POST_request(self, client):
    client.post('/lists/add',
      data={'item_text': 'A new list item'}
    )
    assert Item.objects.count() == 1
    new_item = Item.objects.first()
    assert new_item.text == 'A new list item'

  @pytest.mark.django_db
  def test_new_list_redirects_after_POST(self, client):
    response = client.post('/lists/add',
      data={'item_text': 'A new list item'}
    )

    assert response.status_code == 302
    assert response['Location'] == testserver_url + '/lists/the-only-list-in-the-world/'