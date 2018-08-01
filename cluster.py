import pandas as pd
import numpy as np
from random import randint
from scipy import linalg

feature_set = pd.read_csv('data/data.csv')

# TODO: make sure K-means imlementation is correct or use built-in
def run_clustering(k):
    X = np.transpose(feature_set.values)
    m = X.shape[0]

    # Intitialize Cenroids
    centroids = []
    for i in range(0,k):
        j = randint(0,m-1)
        centroids.append(X[j,:])
        # List of array vectors

    # Run K-Means
    num_iters = 10
    assign = np.array([0]*m)
    for n in range(0,num_iters):
        for i in range(0,m):
            c_dist = []
            for c in range(0,k):
                c_dist.append(np.power((linalg.norm(X[i,:]-centroids[c])),2))
            c_dist = np.array(c_dist)
            c_index = np.unravel_index(np.argmin(c_dist),c_dist.shape)[0]
            assign[i] = c_index

        for j in range(0,k):
            assign_logic = np.array(np.equal(assign,j),dtype=int).reshape(m,1)
            this_assign = np.multiply(assign_logic,X)
            centroids[j] = np.mean(this_assign,axis=0)

    assign_data = {'name':feature_set.columns,'cluster':assign}
    assign_data = pd.DataFrame(assign_data,columns=['name','cluster'])
    assign_data.to_csv('data/assign.csv',index=False)
    centroid_data = np.array(centroids)
    np.savetxt('data/centroids.csv', centroid_data, delimiter=',')

def compute_cost():
    centroids = np.genfromtxt('data/centroids.csv',delimiter=',')
    assign = pd.read_csv('data/assign.csv').values[:,1]
    X = np.transpose(feature_set.values)
    m = X.shape[0]
    cost_sum = 0
    for i in range(0,m):
        distort = np.power(linalg.norm(X[i,:] - centroids[assign[i]]),2)
        cost_sum = cost_sum + distort
    return cost_sum / m

# K value analysis
k_max = 20
k_vals = list(range(1,k_max + 1))
cost_vals = [0] * k_max
for k in k_vals:
    run_clustering(k)
    cost_vals[k-1] = compute_cost()

import matplotlib.pyplot as plt
ax = plt.axes()
plt.plot(k_vals,cost_vals)
plt.show()
