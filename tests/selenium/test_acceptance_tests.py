import pytest
from selenium.webdriver.common.keys import Keys
import re 

def check_for_row_in_list_table(browser, row_text):
  table = browser.find_element_by_id('id_list_table')
  rows = table.find_elements_by_tag_name('tr')
  assert row_text in [row.text for row in rows]
  

def test_can_start_a_list_and_retrieve_it_later(bf, live_server):
  # Edith has heard about a cool new online to-do app. She goes
  # to check out its homepage
  b = bf.get()
  b.get(live_server.url)

  # She notices the page title and the header mention to-do lists
  assert 'To-Do' in b.title, 'Browser title was ' + b.title
  header_text = b.find_element_by_tag_name('h1').text
  assert 'To-Do' in header_text

  # She is invited to enter a to-do item straight away
  inputbox = b.find_element_by_id('id_new_item')
  assert inputbox.get_attribute('placeholder') == 'Enter a to-do item'

  # She types "Buy peacock feathers" into a text box (Edith's hobby
  # is tying fly-fishing lures)
  inputbox.send_keys('Buy peacock feathers')

  # When she hits enter, the page updates, and now the page lists
  # "1: Buy peacock feathers" as an item in a to-do list
  inputbox.send_keys(Keys.ENTER)
  edith_list_url = b.current_url
  assert re.match(live_server.url + '/lists/.+', edith_list_url), edith_list_url
  check_for_row_in_list_table(b, '1: Buy peacock feathers')
  
  # There is still a text box inviting her to add another item. She
  # enters "Use peacock feathers to make a fly" (Edith is very methodical)
  inputbox = b.find_element_by_id('id_new_item')
  inputbox.send_keys('Use peacock feathers to make a fly')
  inputbox.send_keys(Keys.ENTER)

  # The page updates again, and now shows both items on her list
  check_for_row_in_list_table(b, '1: Buy peacock feathers')
  check_for_row_in_list_table(b, '2: Use peacock feathers to make a fly')
  
  # Now a new user, Francis, comes along to the site.

  ## We use a new browser session to make sure that no information
  ## of Edith's is coming through from cookies etc
  b.close()
  b = bf.get()

  # Francis visits the home page. There is no sign of Edith's
  # list
  b.get(live_server.url)
  page_text = b.find_element_by_tag_name('body').text
  assert 'Buy peacock feathers' not in page_text
  assert 'make a fly' not in page_text

  # Francis starts a new list by entering a new item. He
  # is less interesting than Edith...
  inputbox = b.find_element_by_id('id_new_item')
  inputbox.send_keys('Buy milk')
  inputbox.send_keys(Keys.ENTER)

  # Francis gets his own unique URL
  francis_list_url = b.current_url
  assert re.match(live_server.url + '/lists/.+', francis_list_url)
  assert francis_list_url != edith_list_url

  # Again, there is no trace of Edith's list
  page_text = b.find_element_by_tag_name('body').text
  assert 'Buy peacock feathers' not in page_text
  assert 'make a fly' not in page_text

  # Satisfied, they both go back to sleep