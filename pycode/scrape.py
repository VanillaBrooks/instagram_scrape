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

		self.all_data = [] # a collection of all the scraped user data held in a dictionary
		#
		# TODO: The executable_path will have to be reconfigured for the
		# 		currnet location in instagram_scrape/webdrivers/geckodriver.exe
		#
		self.driver = Firefox(executable_path='geckodriver', options=options,capabilities =caps) # driver to access webpages

		self.username = None

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
		# if we have previously scraped data for a user lets add it to the total data before we
		if self.username is not None:
			self.all_data.append({'username': self.username, 'data': self.user_data})

		self.user_data = {} # stores all the current information about the user being scraped

		# direct to a new webpage of users
		url_to_user = r'https://www.instagram.com/' + username
		self.driver.get(url_to_user)
		self.username = username
		pass

	def get_user_stats(self):
		posts = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='react-root']/section/main/div/header/section/ul/li[1]/span/span"))).text
		followers = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a/span"))).text
		following = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='react-root']/section/main/div/header/section/ul/li[3]/a"))).text

		self.user_data['posts'] = posts
		self.user_data['follower_count'] = followers
		self.user_data['following_count'] = following

	def get_image_data(self):
		# try to open first n images and gather captions
		previous_count = 0
		current_count = 1

		self.user_data['posts'] = []
									# {'comments': [], likecount: 0}
		# make sure the first few images are loaded
		WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(By.PARTIAL_LINK_TEXT, "/p/"))

		# while we continue to find more and more pictures
		while current_count - previous_count:
			# set the previous count of images to what it was before
			previous_count = current_count

			# and now find a list() of the total number of links on a page
			all_picture_link_elements = self.driver.find_elements(By.PARTIAL_LINK_TEXT "/p/")
			# get the length of all the elements that contain pictures
			current_count = len(all_picture_link_elements)

			# we go back to an element and send the page down since
			# page down requires that it be done to an element class
			all_picture_link_elements[0].send_keys(Keys.PAGE_DOWN)

		# we are now outside of the loop so lets do stuff with all_picture_link_elements
		# AKA lets parse each link in the list


		for element in all_picture_link_elements:
			element.click()
			likecount = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(By.XPATH, "/html/body/div[2]/div[2]/div/article/div[2]/section[2]/div/div[2]/button/span")).text

			username_comment_elements = self.driver.find_elements(By.XPATH, "/html/body/div[2]/div[2]/div/article/div[2]/div[1]/ul/li/div/div/div/h2/a")
			comment_text_elements = self.driver.find_elements(By.XPATH,"/html/body/div[2]/div[2]/div/article/div[2]/div[1]/ul/li/div/div/div/span")

			if len(comment_text_elements) != len(username_comment_elements):
				raise ValueError('holy shit they are supposed to be the same length and they are not some bad shit happened')

			list_of_comment_data = []

			for i in range(len(comment_text_elements)):
				list_of_comment_data.append([ username_comment_elements[i].get_attribute('title') , comment_text_elements[i].text])



			self.user_data['posts'].append(    {'comments': list_of_comment_data), 'like_count': likecount}       )











		def clear_data_dict(self):
			self.user_data = {}

	def get_user_followers(self):
		# find all the followers that a user has so that we can scrape them
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
