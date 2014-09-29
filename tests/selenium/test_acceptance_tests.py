import pytest
from selenium.webdriver.common.keys import Keys

def test_can_start_a_list_and_retrieve_it_later(b):
    # Edith has heard about a cool new online to-do app. She goes
    # to check out its homepage
    b.get('http://localhost:8111')

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

    table = b.find_element_by_id('id_list_table')
    rows = b.find_elements_by_tag_name('tr')
    assert '1: Buy peacock feathers' in [row.text for row in rows]
    
    # There is still a text box inviting her to add another item. She
    # enters "Use peacock feathers to make a fly" (Edith is very methodical)
    inputbox = b.find_element_by_id('id_new_item')
    inputbox.send_keys('Use peacock feathers to make a fly')
    inputbox.send_keys(Keys.ENTER)

    # The page updates again, and now shows both items on her list
    table = b.find_element_by_id('id_list_table')
    rows = table.find_elements_by_tag_name('tr')
    assert '1: Buy peacock feathers' in [row.text for row in rows]
    assert '2: Use peacock feathers to make a fly' in [row.text for row in rows]

    # Edith wonders whether the site will remember her list. Then she sees
    # that the site has generated a unique URL for her -- there is some
    # explanatory text to that effect.
    raise AssertionError('Finish the test!')

    # She visits that URL - her to-do list is still there.

    # Satisfied, she goes back to sleep
