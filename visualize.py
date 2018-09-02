#! /usr/bin/python


import argparse
import pandas as pd
import numpy as np
from sklearn.manifold import TSNE

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--vecs", \
help="high-dim vectors to be reduced; in a file", required=True)
parser.add_argument("-n", "--dim", \
help="number of dimensions in reduced form", required=False, default=2)
parser.add_argument("-c", "--clusters",\
help="point cluster assignments; in a file", required=False, default="")
parser.add_argument("-o", "--output",\
help="location to store vectors", required=False, default="")

args = vars(parser.parse_args())

#vecs_file = (sys.argv[1])
vecs_file = args['vecs']
red_dim = int(args['dim'])
cluster_file = args['clusters']
vecs_out = args['output']

# constrain dimension
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
if vecs_out != "":
    print('saving reduced data...')
    data = {'name':names,'subscribers': subscribers}
    data_reduce = pd.DataFrame(data,columns=['name','subscribers'])

    if red_dim == 1:
        data_reduce['x'] = vecs_reduce[:,0]
        data_reduce.to_csv(vecs_out, encoding='utf-8',\
        columns=['name','subscribers','x'], index=False)
    elif red_dim == 2:
        data_reduce['x'] = vecs_reduce[:,0]
        data_reduce['y'] = vecs_reduce[:,1]
        data_reduce.to_csv(vecs_out, encoding='utf-8',\
        columns=['name','subscribers','x','y'], index=False)
    elif red_dim == 3:
        data_reduce['x'] = vecs_reduce[:,0]
        data_reduce['y'] = vecs_reduce[:,1]
        data_reduce['z'] = vecs_reduce[:,2]
        data_reduce.to_csv(vecs_out, encoding='utf-8',\
        columns=['name','subscribers','x','y','z'], index=False)

import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, plot

print('plotting...')

plot_colors = subscribers

if (cluster_file != ''):
    print('found cluster assignments')
    clusters = pd.read_csv(cluster_file)['cluster'] # assume same order

    color_map = {
    0.0: '#e6f2ff', 1.0: '#99ccff',
    2.0: '#ccccff', 3.0: '#cc99ff',
    4.0: '#ff99ff', 5.0: '#ff6699',
    6.0: '#ff9966', 7.0: '#ff6600',
    8.0: '#ff5050', 9.0: '#ff0000',
    10.0: '#18ff01', 11.0: '#6a2b11',
    12.0: '#b7bf05', 13.0: '#2859c1'}
    # supports up to 14 clusters

    plot_colors = clusters.map(color_map)

if (red_dim == 2):
    plot([go.Scatter(
        x = vecs_reduce[:,0],
        y = vecs_reduce[:,1],
        mode = 'markers',
        marker = dict(
            size = 6,
            color = plot_colors,
            colorscale='magma',
            showscale=True
        ),
        text = names
    )], filename="figures/simple-vis.html")
elif (red_dim == 3):
    plot([go.Scatter3d(
        x = vecs_reduce[:,0],
        y = vecs_reduce[:,1],
        z = vecs_reduce[:,2],
        mode = 'markers',
        marker = dict(
            size = 6,
            color = plot_colors,
            colorscale='magma',
            showscale=True
        ),
        text = names
    )], filename="figures/simple-vis.html")
