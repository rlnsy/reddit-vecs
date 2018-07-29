#%matplotlib notebook
import pandas as pd
import numpy as np
from scipy import linalg
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

count_set = pd.read_csv('data/counts.csv')
feature_set = pd.read_csv('data/data.csv')

#count_set.plot(stacked=False)

#feature_set[140:200].plot.barh(stacked=True)

#plt.show()

#PCA
X = np.transpose(feature_set.values)
m = X.size
covar_mat = np.dot(np.transpose(X),X) / m
U, S, V = linalg.svd(covar_mat)
U_reduce = U[:,0:3]
Z_all = np.dot(X,U_reduce)


ax = plt.axes(projection='3d')
x = Z_all[:,0]
y = Z_all[:,1]
z = Z_all[:,2]
ax.scatter(x, y, z, c=z, cmap='viridis', linewidth=0.5);
plt.show()
