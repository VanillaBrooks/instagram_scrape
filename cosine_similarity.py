import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from scipy.spatial.distance import pdist, squareform

import requests


import requests

# Fill in your details here to be posted to the login form.
payload = {
    'inUserName': 'slayer_man_226',
    'inUserPass': 'sailboat123'
}

# Use 'with' to ensure the session context is closed after use.
with requests.Session() as s:
    p = s.post('LOGIN_URL', data=payload)
    # print the html returned or something more intelligent to see if it's a successful login page.
    print p.text

    # An authorised request.
    r = s.get('A protected web page url')
    print r.text
