from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.wait import WebDriverWait

#https://developer.mozilla.org/en-US/docs/Mozilla/Firefox/Headless_mode



class InstagramScraper():
	def __init__(self):
		# configure a headless webdriver
		options = Options()
		options.add_argument('-headless')
		self.driver = Firefox(executable_path='geckodriver', options=options)
		wait = WebDriverWait(self.driver, timeout=10)

	def __example(self):
		self.driver.get('http://www.google.com')
		wait.until(expected.visibility_of_element_located((By.NAME, 'q'))).send_keys('headless firefox' + Keys.ENTER)
		wait.until(expected.visibility_of_element_located((By.CSS_SELECTOR, '#ires a'))).click()
		print(self.driver.page_source)
		self.driver.quit()

	def authenticate(self):
		# login to https://www.instagram.com/accounts/login/?source=auth_switcher
		pass

	def open_user(self, username):
		# direct to a new webpage of users
		url_to_user = r'https://www.instagram.com/' + username
		pass

	def get_image_data(self):
		# try to open first n images and gather captions
		pass

	def get_user_stats(self):
		# fetch followers / follows / **posts**
		# this reduces strain on rescraping the system
		pass
