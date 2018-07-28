import pandas as pd
import matplotlib.pyplot as plt

count_set = pd.read_excel('data/counts.xlsx')
feature_set = pd.read_excel('data/data.xlsx')

count_set.plot(stacked=False)

feature_set[140:200].plot.barh(stacked=True)

plt.show()
