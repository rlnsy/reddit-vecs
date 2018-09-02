# Reduces and plots vectors
# AGUMENTS: Vectors filename
# reduction_dimension (dimension of reduced vectors, default=2)

import sys
import pandas as pd
import numpy as np
from sklearn.manifold import TSNE

vecs_file = (sys.argv[1])

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

print('Reducing vectors in ' + vecs_file + ' with n=' + str(red_dim));

vecs_df = pd.read_csv(vecs_file)
subscribers = vecs_df['subscribers']
names = vecs_df['name']

vecs_df.drop('subscribers', 1, inplace=True)
vecs_df.drop('name', 1, inplace=True)
vecs = vecs_df.values

dists = np.dot(vecs, vecs.T)
vecs_reduce = TSNE(n_components=red_dim).fit_transform(dists)

# saving reductions

#if red_dim == 1:
    #data_reduce['x'] = vecs_reduce[:,0]
    #data_reduce.to_csv(content_dir + '/vecs_1d.csv', encoding='utf-8',\
    #columns=['name','subscribers','x'], index=False)
#elif red_dim == 2:
    #data_reduce['x'] = vecs_reduce[:,0]
    #data_reduce['y'] = vecs_reduce[:,1]
    #data_reduce.to_csv(content_dir + '/vecs_2d.csv', encoding='utf-8',\
    #columns=['name','subscribers','x','y'], index=False)
#elif red_dim == 3:
    #data_reduce['x'] = vecs_reduce[:,0]
    #data_reduce['y'] = vecs_reduce[:,1]
    #data_reduce['z'] = vecs_reduce[:,2]
    #data_reduce.to_csv(content_dir + '/vecs_3d.csv', encoding='utf-8',\
    #columns=['name','subscribers','x','y','z'], index=False)

import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, plot

if (red_dim == 2):
    plot([go.Scatter(
        x = vecs_reduce[:,0],
        y = vecs_reduce[:,1],
        mode = 'markers',
        marker = dict(
            size = 6,
            color = subscribers,
            colorscale='magma',
            showscale=True
        ),
        text = names
    )], filename="figures/simple-vis.html")
