import pandas as pd
import matplotlib.pyplot as plt

count_set = pd.read_excel('data/data.xlsx')

plt.figure(); count_set.plot();


plt.show()
