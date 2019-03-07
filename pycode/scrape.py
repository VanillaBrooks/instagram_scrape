from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
import selenium

import json
import string
import time

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
		self.driver = Firefox(executable_path='webdrivers/geckodriver.exe', options=options,capabilities =caps) # driver to access webpages

		self.username = None

	# log a user in from either input arguments or stored json
	def authenticate(self, username=False, password=False):
		LOGIN_URL = 'https://www.instagram.com/accounts/login/'
		# self.driver.switch_to.frame(self.driver.find_element_by_name('spout-unit-iframe')) # switch iframe code

		# get login details from json if none specified
		if not (username and password):
			with open (r'authentication/config.json') as file:
				user_details = json.load(file)
				username = user_details['username']
				password = user_details['password']

		self.driver.get(LOGIN_URL) # load up the instagram login page

		# username field
		username_elem = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@name='username']")))
		username_elem.click()
		username_elem.send_keys(username) # send the keys for the username

		# password field
		password_elem = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@name='password']")))
		password_elem.click()
		password_elem.send_keys(password) # send the keys for the password

		# click the submit button
		submit_elem = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@type='submit']")))
		submit_elem.click()

		# when you launch without cookies it promtps you to set stuff up. this clicks "not now"
		not_now_elem = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/span/div/div[2]/a[2]")))
		not_now_elem.click()

	# open a user's instagram page
	def open_user(self, username):
		print('opened a new user {}'.format(username))

		# if we have previously scraped data for a user lets add it to the total data before we
		if self.username is not None:
			self.all_data.append({'username': self.username, 'data': self.user_data})

		self.user_data = {} # stores all the current information about the user being scraped

		# direct to a new webpage of users
		self.url_to_user = r'https://www.instagram.com/' + username
		self.driver.get(self.url_to_user)
		self.username = username

		print('loaded user {} , exiting function'.format(self.url_to_user))

	# get profile stats for a user
	def get_user_stats(self):
		# function to remove the potential punctuation in a element
		def remove_punctuation(input_elem):
			return input_elem.text.translate(str.maketrans('', '', string.punctuation))

		# XPATHS for post \ follower \ following counts
		posts = remove_punctuation(WebDriverWait(self.driver, 10).until(\
			EC.presence_of_element_located((\
			By.XPATH, "//*[@id='react-root']/section/main/div/header/section/ul/li[1]/span/span"))))
		followers = remove_punctuation(WebDriverWait(self.driver, 10).until(\
			EC.presence_of_element_located((\
			By.XPATH, "//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a/span"))))
		following = remove_punctuation(WebDriverWait(self.driver, 10).until(\
			EC.presence_of_element_located((\
			By.XPATH, "/html/body/span/section/main/div/header/section/ul/li[3]/a/span"))))


		# for debug: print out all the data for the currently loaded user
		print(f'the user data:\nposts : {posts}\nfollowers: {followers}\nfollowing: {following}')

		# store data in the main dictionary for later
		self.user_data['post_count'] = int(posts)
		self.user_data['follower_count'] = int(followers)
		self.user_data['following_count'] = int(following)

	def get_image_data(self):
		# try to open first n images and gather captions
		previous_count = 0
		current_count = 1

		self.user_data['posts'] = []
									# {'comments': [], likecount: 0}
		# make sure the first few images are loaded
		WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//a[contains(@href, "/p/")]')))
		#'//a[contains(@href, "WO20")]'
		print('here')

		body_elem = self.driver.find_element(By.XPATH, '/html')
		picture_links = set()
		picture_url_xpath = '//a[contains(@href, "/p/")]'
		pics = self.driver.find_elements(By.XPATH, picture_url_xpath)

		# push down the user's page while we are still finding more pictures
		while current_count < self.user_data['post_count']:
			print(f'in loop with a picture count of {current_count}')
			# set the previous count of images to what it was before
			previous_count = current_count

			# and now find a list() of the total number of links on a page
			all_picture_link_elements = self.driver.find_elements(By.XPATH, picture_url_xpath)
			# get the length of all the elements that contain pictures
			picture_links.update({i.get_attribute('href') for i in all_picture_link_elements if i not in picture_links})
			current_count = len(picture_links)
			print('total len: {} current len: {}'.format(current_count, len(all_picture_link_elements)))

			# we go back to an element and send the page down since
			# page down requires that it be done to an element class

			for _ in range(3):
				time.sleep(.1)
				print('scroll...')
				body_elem.send_keys(Keys.PAGE_DOWN)

		# we are now outside of the loop so lets do stuff with all_picture_link_elements
		# AKA lets parse each link in the list

		print(f'about to parse through the {len(all_picture_link_elements)} pictures found')
		# print('the picture links are')
		# import pprint
		# pprint.pprint(picture_links)
		old_caption = False	 # ensures the first run of the while loop stops early

		# open each url and collect metadata from the post
		for url in picture_links:
			# url = self.url_to_user + element.get_attribute('href')
			print(f'url to picture is {url}')
			self.driver.get(url)

			text_path = "/html/body/span/section/main/div/div/article/div/div/ul/li/div/div/div/span"

			# run this loop to ensure that the page being parsed was not equal
			# to the last page that was just scraped. If this loop does not run
			# then we will parse the same page over and over before the page
			# ever even loads for the first time
			while True:
				# catch an exception that happens from reloading the page while scraping it
				try:
					caption_text = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, text_path))).text
				except StaleElementReferenceException:
					print('Refresh page exception ! ')
					continue

				# if its the first time in the for loop we can just exit now
				if old_caption == False: break

				# get all text from the comments
				# print('::::the caption is {} \n'.format(caption_text))
				# print('::::the old caption was {}'.format(old_caption))

				if caption_text == old_caption:
					# print('!!!they match, try again')
					continue
				else:
					# print('!!!!dont match, break')
					break


			text = self.driver.find_elements(By.XPATH, text_path)
			text = [i.text for i in text]
			caption_text = text.pop(0)

			like_path = "/html/body/span/section/main/div/div/article/div[2]/section[2]/div/div/a/span"
			try: likecount = self.driver.find_element(By.XPATH, like_path).text
			except NoSuchElementException: likecount = 0 	# post uses views instead of likes

			# get all users that have commented
			users_path = "/html/body/span/section/main/div/div/article/div[2]/div[1]/ul/li/div/div/div/h3/a"
			users = self.driver.find_elements(By.XPATH, users_path)
			users = [i.text for i in users]


			print(f"like count {likecount} usernames {len(users)} text{len(text)}")

			print(users)
			print(text)
			print('\n\n\n\n')

			# the length of comment text is 1 more than usernames of comments
			# the main caption is included in the comments, but not poster name
			if len(text) != len(users):
				raise ValueError('holy shit they are supposed to be the same length and they are not some bad shit happened')

			parsed_comment_data = []

			for i in range(len(text)):
				parsed_comment_data.append([users[i] , text[i]])

			self.user_data['posts'].append({'comments': parsed_comment_data, 'like_count': likecount, 'caption':caption_text})

			first_run = False # enable additional checks now
			old_caption = caption_text

	def clear_data_dict(self):
		self.user_data = {}

#
#	THIS FUNCTION NEEDS TO BE FIXED TO FIND FOLLOWING
#
	def get_user_followers(self):
		following_path = '/html/body/span/section/main/div/header/section/ul/li[3]/a/span'
		user_path = '/html/body/div[2]/div/div[2]/ul/div/li/div/div[2]/div[1]/div/div/a'
		user_path = '/html/body/div[2]/div/div[2]/ul/div/li/div/div[1]/div[1]/a'
		see_all_suggestions_path = '/html/body/div[2]/div/div[2]/div[4]/a'
		header_path = '/html/body/div[2]/div/div[2]'

		# /html/body/div[2]/div/div[2]/ul/div/li[119]/div/div[1]/div[2]/div[1]/a

		following_elem= WebDriverWait(self.driver, 10).until(\
			EC.presence_of_element_located((\
			By.XPATH, following_path)))
		following_elem.click()

		count = 0
		all_users = set()
		WebDriverWait(self.driver, 10).until(\
			EC.presence_of_element_located((\
			By.XPATH, user_path)))

		import pprint
		old_vis = False
		while count < self.user_data['following_count']:
			visible = self.driver.find_elements(By.XPATH, user_path)

			try:visible_set = {i.get_attribute('href') for i in visible}
			except Exception: continue
			all_users.update(visible_set)
			count = len(all_users)
			print(f'current count: {count} percentage: {100*count/self.user_data["following_count"]}')

			self.driver.find_element(By.XPATH, header_path).send_keys(Keys.PAGE_DOWN)
			time.sleep(.1)


if __name__ == "__main__":
	start = time.time()

	i = InstagramScraper()
	i.authenticate()
	i.open_user('ayaanakano')
	i.get_user_stats()
	i.get_user_followers()
	i.get_image_data()

	end = time.time()

	print('runtime: {end-start}')
