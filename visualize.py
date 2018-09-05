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
parser.add_argument("-r", "--reduce",\
help="whether or not to reduce input before plotting", required=False, default="true")
parser.add_argument("-o", "--output",\
help="location to store vectors", required=False, default="")

args = vars(parser.parse_args())

#vecs_file = (sys.argv[1])
vecs_file = args['vecs']
red_dim = int(args['dim'])
cluster_file = args['clusters']
reduce_input = args['reduce'] == 'true'
vecs_out = args['output']

# constrain dimension
if red_dim < 1:
    red_dim = 2
elif red_dim > 3:
    red_dim = 3

vecs_df = pd.read_csv(vecs_file)
subscribers = vecs_df['subscribers']
names = vecs_df['name']

vecs_df.drop('subscribers', 1, inplace=True)
vecs_df.drop('name', 1, inplace=True)
vecs = vecs_df.values
vecs_reduce = vecs

if (reduce_input):
    print('Reducing vectors in ' + vecs_file + ' with n=' + str(red_dim));

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

    num_clusters = len(np.unique(clusters.values))

    import random
    def gen_hex_colour_code():
        return ''.join([random.choice('0123456789ABCDEF') for x in range(6)])

    color_map = {}
    for c in range(0,num_clusters):
        color_map[float(c)] = gen_hex_colour_code()

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
