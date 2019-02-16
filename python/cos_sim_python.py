import numpy as np
import sklearn
import sklearn.feature_extraction
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
	transformed_vector = vector.fit_transform([_list2str(captions_list_1), _list2str(captions_list_2)])
	# calculate cos dist for element
	distances = scipy.spatial.distance.pdist(transformed_vector.toarray(), 'cosine')
	# convert to [nxn] array of distnaces
	# this shows the relative similarity of each row to the others
	cosine_similarity = scipy.spatial.distance.squareform(distances)

	return cosine_similarity


if __name__ == '__main__':
	list_1 = 'sample phrase'.lower().split()
	list_2 = 'sample here'.lower().split()

	result = cos_sim(list_1, list_2)
	print(result)
