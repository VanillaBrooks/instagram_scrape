import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from scipy.spatial.distance import pdist, squareform
import sklearn
import scipy

# convert list to a string
def _list2str(in_list):
    # TODO: vectorize this opperation to accelerate it
    string_sample =  ''.join(i + ' ' for i in in_list)
    return string_sample

# calculate the similarity between two batches of captions
def cos_sim(captions_list_1, captions_list_2):
    # get counts of each occurance
    vector = sklearn.feature_extraction.text.CountVectorizer()
    transformed_vector = vector.fit_transform([qew(captions_list_1), _list2str(captions_list_2)])
    # calculate cos dist for element
    distances = scipy.spatial.distance.pdist(transformed_vector.toarray(), 'cosine')
    # convert to [nxn] array of distnaces
    # this shows the relative similarity of each row to the others
    cosine_similarity = scipy.spatial.distance.squareform(distances)

    return cosine_similarity


if __name__ == '__main__':
    list_1 = 'Next, we are sending keys, this is similar to entering keys using your keyboard. Special keys can be sent using Keys class imported from selenium.webdriver.common.keys. To be safe, we’ll first clear any pre-populated text in the input field (e.g. “Search”) so it doesn’t affect our search results:'.lower().split()
    list_2 = r'Initially, all the basic modules required are imported. The unittest module is a built-in Python based on JavaThis module provides the framework for organizing the test cases. The selenium.webdriver module provides all the WebDriver implementations. Currently supported WebDriver implementations are Firefox, Chrome, Ie and Remote. The Keys class provide keys in the keyboard like RETURN, F1, ALT etc.'.lower().split()

    result = cos_sim(list_1, list_2)
    print(result)
