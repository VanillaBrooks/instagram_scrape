import selenium
from selenium.webdriver.common.keys import Keys

class InstagramScraper():
    def __init__(self):
        self.driver = webdriver.Chrome()
        # other driver configurations such as:
        #   prematurely scrape the webpage
        #   dont load images
        #
        pass

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

    
