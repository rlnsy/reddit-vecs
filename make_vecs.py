# CONTENT VECTORIZER
# uses TFIDF vectorization techniques to produce hight dimensionl content vectors
# and then reduces them using t-SNE. Saved in relative vecs.csv
# ARGUMENTS: content_directory (dir to read files from - must contain content
#   and reference files)

import sys
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.manifold import TSNE

content_dir = sys.argv[1]

files_store = open(content_dir + '/files.pickle','rb')
files_list = pickle.load(files_store)
vectorizer = TfidfVectorizer(input='filename',stop_words='english',lowercase=True, strip_accents='unicode', smooth_idf=True,sublinear_tf=False, use_idf=True, ngram_range=(1,2),min_df=2)
vecs = vectorizer.fit_transform(files_list)
dists = (vecs * vecs.T).todense()
vecs_2d = TSNE(n_components=2).fit_transform(dists)

import pandas as pd
names_store = open(content_dir + '/names.pickle','rb')
names = pickle.load(names_store)
subscriber_counts_store = open(content_dir + '/subscribers.pickle','rb')
subscriber_counts = pickle.load(subscriber_counts_store)
data = {'name':names, 'x':vecs_2d[:,0], 'y':vecs_2d[:,1], 'subscribers': subscriber_counts}
df = pd.DataFrame(data,columns=['name','x','y','subscribers'])
df.to_csv(content_dir + '/vecs.csv', encoding='utf-8',columns=['name','x','y','subscribers'], index=False)
