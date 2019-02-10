from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import json

#https://developer.mozilla.org/en-US/docs/Mozilla/Firefox/Headless_mode



class InstagramScraper():
	def __init__(self):
		options = Options()
		# options.add_argument('-headless')	# headless mode so the window doesnt actually appear (disabled currently)
		caps = DesiredCapabilities().FIREFOX
		caps["pageLoadStrategy"] = "none"	# scrape page prematurely

		self.driver = Firefox(executable_path='geckodriver', options=options,capabilities =caps) # driver to access webpages

	# code from mozilla
	def __example(self):
		self.driver.get('http://www.google.com')
		wait.until(expected.visibility_of_element_located((By.NAME, 'q'))).send_keys('headless firefox' + Keys.ENTER)
		wait.until(expected.visibility_of_element_located((By.CSS_SELECTOR, '#ires a'))).click()
		print(self.driver.page_source)
		self.driver.quit()

	def authenticate(self, username=False, password=False):
		LOGIN_URL = 'https://www.instagram.com/accounts/login/'

		# get login details from json if none specified
		if not (username and password):
			with open (r'authentication/config.json') as file:
				user_details = json.load(file)
				username = user_details['username']
				password = user_details['password']

		self.driver.get(LOGIN_URL) # load up the instagram login page

		# TODO: Fix this xpath (instagram uses .js to create new ids each time)
		username = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[contains(@aria-label, ‘Phone number, username, or email’)]")))
		username.click()
		username.send_keys(username) # send the keys for the username

		password = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[contains(@aria-label, ‘Password’)]")))
		passsword.click()
		password.send_keys(password) # send the keys for the password

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

# attempt to do it with requests
def connection():
	import requests
	with open (r'authentication/config.json') as file:
		user_details = json.load(file)
		username = user_details['username']
		password = user_details['password']

	import bs4

	req = requests.Session()
	base = req.get("https://instagram.com")
	req.headers = {'user-agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'}
	req.headers.update({"Referer": "https://instagram.com"})

	req.headers.update({'X-CSRFToken': base.cookies['csrftoken']})

	login = req.post('https://instagram.com/login', data={"Username": "slayer_man_226", "Password": "sailboat123"}, allow_redirects=True)

	req.headers.update({'X-CSRFToken' : login.cookies['csrftoken']})

	result = req.get("https://instagram.com/ayaanakano", auth=(username, password))

	soup = bs4.BeautifulSoup(result.text)

	with open ('html.txt', 'wb') as f:
		f.write(soup.prettify().encode("utf8"))


if __name__ == "__main__":
	i = InstagramScraper()
	i.authenticate()
