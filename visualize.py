import pandas as pd
import matplotlib.pyplot as plt

count_set = pd.read_csv('data/counts.csv')
feature_set = pd.read_csv('data/data.csv')

count_set.plot(stacked=False)

feature_set[140:200].plot.barh(stacked=True)

plt.show()
