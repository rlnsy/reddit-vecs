# CONTENT VECTORIZER
# uses TFIDF vectorization techniques to produce hight dimensionl content vectors
# and then reduces them using t-SNE. Saved in relative vecs.csv
# ARGUMENTS: content_directory (dir to read files from - must contain content
#   and reference files),
# (optional) reduction_dimension (dimension of reduced vectors, default=2)

import sys
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.manifold import TSNE

def vectorize_and_reduce(content_dir, dim):
    files_store = open(content_dir + '/files.pickle','rb')
    files_list = pickle.load(files_store)
    vectorizer = TfidfVectorizer(input='filename',stop_words='english',lowercase=True,\
    strip_accents='unicode', smooth_idf=True,sublinear_tf=False, use_idf=True, ngram_range=(1,2),min_df=2)
    vecs = vectorizer.fit_transform(files_list)
    dists = (vecs * vecs.T).todense()
    vecs_reduce = TSNE(n_components=dim).fit_transform(dists)
    vecs_all = vecs.todense()
    return vecs_reduce, vecs_all

content_dir = sys.argv[1]
red_dim = 2

# check dimension values
try:
    red_dim = int(sys.argv[2])
except IndexError:
    print('No dimension specified; using n=2')

if red_dim < 1:
    red_dim = 2
elif red_dim > 3:
    red_dim = 3

print('Vectorizing and reducing data from ' + content_dir + ' with n=' + str(red_dim))

# execute the methods
vecs_reduce, vecs_all = vectorize_and_reduce(content_dir,red_dim)

# save the reduced vectors
import pandas as pd

names_store = open(content_dir + '/names.pickle','rb')
names = pickle.load(names_store)
subscriber_counts_store = open(content_dir + '/subscribers.pickle','rb')
subscriber_counts = pickle.load(subscriber_counts_store)

data = {'name':names,'subscribers': subscriber_counts}
data_reduce = pd.DataFrame(data,columns=['name','subscribers'])

if red_dim == 1:
    data_reduce['x'] = vecs_reduce[:,0]
    data_reduce.to_csv(content_dir + '/vecs.csv', encoding='utf-8',\
    columns=['name','subscribers','x'], index=False)
elif red_dim == 2:
    data_reduce['x'] = vecs_reduce[:,0]
    data_reduce['y'] = vecs_reduce[:,1]
    data_reduce.to_csv(content_dir + '/vecs.csv', encoding='utf-8',\
    columns=['name','subscribers','x','y'], index=False)
elif red_dim == 3:
    data_reduce['x'] = vecs_reduce[:,0]
    data_reduce['y'] = vecs_reduce[:,1]
    data_reduce['z'] = vecs_reduce[:,2]
    data_reduce.to_csv(content_dir + '/vecs.csv', encoding='utf-8',\
    columns=['name','subscribers','x','y','z'], index=False)

# save the sparse data matrix
data_all = pd.DataFrame(data,columns=['name','subscribers'])
vec_columns = []
for i in range(0, vecs_all.shape[1]):
    label = 'dim' + str(i)
    data_all[label] = vecs_all[:,i]
    vec_columns.append(label)
data_all.to_csv(content_dir + '/vecs_all.csv',encoding='utf-8',\
columns=(['name','subscribers'] + vec_columns), index=False)
