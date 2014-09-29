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
    list_ = List.objects.create()
    response = client.get('/lists/%d/' % (list_.id))
    template_names = [t.name for t in response.templates]
    assert 'list.html' in template_names

  @pytest.mark.django_db
  def test_list_view_displays_all_user_list_items(self, client):
    user_list = List.objects.create()
    Item.objects.create(text='itemey 1', list=user_list)
    Item.objects.create(text='itemey 2', list=user_list)
    other_list = List.objects.create()
    Item.objects.create(text='other list item 1', list=other_list)
    Item.objects.create(text='other list item 2', list=other_list)

    response = client.get('/lists/%d/' % (user_list.id))

    assert 'itemey 1' in response.content.decode()
    assert 'itemey 2' in response.content.decode()
    assert 'other list item 1' not in response.content.decode()
    assert 'other list item 2' not in response.content.decode()

  @pytest.mark.django_db
  def test_passes_correct_list_to_template(self, client):
    other_list = List.objects.create()
    user_list = List.objects.create()
    response = client.get('/lists/%d/' % (user_list.id,))
    assert response.context['list'] == user_list


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
      data={'item_text': 'A new list item'},
    )
    new_list = List.objects.first()

    assert response.status_code == 302
    assert response['Location'] == testserver_url + '/lists/%d/' % (new_list.id)

class TestNewItem(object):

  @pytest.mark.django_db
  def test_can_save_a_POST_request_to_an_existing_list(self, client):
    other_list = List.objects.create()
    user_list = List.objects.create()

    client.post(
      '/lists/%d/add_item' % (user_list.id,),
      data={'item_text': 'A new item for an existing list'}
    )

    assert Item.objects.count() == 1
    new_item = Item.objects.first()
    assert new_item.text == 'A new item for an existing list'
    assert new_item.list == user_list

  @pytest.mark.django_db
  def test_redirects_to_list_view(self, client):
    other_list = List.objects.create()
    user_list = List.objects.create()

    response = client.post(
      '/lists/%d/add_item' % (user_list.id,),
      data={'item_text': 'A new item for an existing list'}
    )

    assert response.status_code == 302
    assert response['Location'] == testserver_url + '/lists/%d/' % (user_list.id)
