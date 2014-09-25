from selenium import webdriver


browser = webdriver.Firefox()
browser.get('http://localhost:8111')

assert 'Django' in browser.title
