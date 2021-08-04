import matplotlib.pyplot as plt
import pickle
import numpy as np
import pandas as pd

ip_addresses = [("New York", "162.243.19.47"), ("Greater Noida", "117.55.243.14"),
                ("Guangzhou", "202.46.34.74"), ("Chitose, Japan", "210.228.48.238"),
                ("Cruseilles, France", "62.212.113.125"), ("Presidente Prudente, Brazil", "177.43.35.247"),
                ("United Kingdom", "88.208.211.65"), ("Australia", "1.1.1.1")]

delays = pickle.load(open("delays.dat", "rb"))
for i in range(delays.shape[1]-1):
    if ip_addresses[i][0] != "Presidente Prudente, Brazil":
        plt.plot(delays[:,0][np.where(delays[:,i+1]<np.nanpercentile(delays[:,i+1], 99))], delays[:,i+1][np.where(delays[:,i+1]<np.nanpercentile(delays[:,i+1], 99))], label=ip_addresses[i][0])

plt.legend()
plt.show()
