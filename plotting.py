import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def plotting(fileName):
    data = pd.read_csv(fileName, names=["min", "average", "max"]) 
    average = data.iloc[:, 1].values
    x = np.arange(len(average))
    plt.plot(x, data)
    plt.show()

plotting('fitness_data_for_plotting1.csv')
