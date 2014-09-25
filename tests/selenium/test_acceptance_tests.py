import pytest

def test_can_start_a_list_and_retrieve_it_later(b):
		# Edith has heard about a cool new online to-do app. She goes
		# to check out its homepage
		b.get('http://localhost:8111')

		# She notices the page title and the header mention to-do lists
		assert 'To-Do' in b.title, 'Browser title was ' + b.title
		raise AssertionError('Finish the test!')

		# She is invited to enter a to-do item straight away

		# She types "Buy peacock feathers" into a text box (Edith's hobby
		# is tying fly-fishing lures)

		# When she hits enter, the page updates, and now the page lists
		# "1: Buy peacock feathers" as an item in a to-do list

		# There is still a text box inviting her to add another item. She
		# enters "Use peacock feathers to make a fly" (Edith is very methodical)

		# The page updates again, and now shows both items on her list

		# Edith wonders whether the site will remember her list. Then she sees
		# that the site has generated a unique URL for her -- there is some
		# explanatory text to that effect.

		# She visits that URL - her to-do list is still there.

		# Satisfied, she goes back to sleep
