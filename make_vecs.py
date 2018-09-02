# CONTENT VECTORIZER
# uses TFIDF vectorization techniques to produce hight dimensionl content vectorsself.
# Saved in relative data.csv
# ARGUMENTS: content_directory (dir to read files from - must contain content
#   and reference files),

import sys
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

content_dir = sys.argv[1]

print('Vectorizing content from ' + content_dir)

files_store = open(content_dir + '/files.pickle','rb')
files_list = pickle.load(files_store)
vectorizer = TfidfVectorizer(input='filename',stop_words='english',lowercase=True,\
strip_accents='unicode', smooth_idf=True,sublinear_tf=False, use_idf=True, ngram_range=(1,2),min_df=2)
vecs_all = vectorizer.fit_transform(files_list).todense()

print(vecs_all.shape)

import time
time.sleep(10000000)

# save the data
import pandas as pd

names_store = open(content_dir + '/names.pickle','rb')
names = pickle.load(names_store)
subscriber_counts_store = open(content_dir + '/subscribers.pickle','rb')
subscriber_counts = pickle.load(subscriber_counts_store)

data = {'name':names,'subscribers': subscriber_counts}
data_reduce = pd.DataFrame(data,columns=['name','subscribers'])

# save the sparse data matrix
data_all = pd.DataFrame(data,columns=['name','subscribers'])
vec_columns = []
for i in range(0, vecs_all.shape[1]):
    label = 'dim' + str(i)
    data_all[label] = vecs_all[:,i]
    vec_columns.append(label)
data_all.to_csv(content_dir + '/data.csv',encoding='utf-8',\
columns=(['name','subscribers'] + vec_columns), index=False)
