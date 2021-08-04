from tcp_latency import measure_latency
import numpy as np
import threading
import time
import pickle
import matplotlib.pyplot as plt

ip_addresses = [("New York", "162.243.19.47"), ("Greater Noida", "117.55.243.14"),
                ("Guangzhou", "202.46.34.74"), ("Chitose, Japan", "210.228.48.238"),
                ("Cruseilles, France", "62.212.113.125"), ("Presidente Prudente, Brazil", "177.43.35.247"),
                ("United Kingdom", "88.208.211.65"), ("Australia", "1.1.1.1")]

# Produce new delays
num_tests = 1000
delays_np = np.zeros((num_tests, len(ip_addresses)+1))
pickle.dump(delays_np, open("delays.dat", "wb"))

initial_time_stamp = time.time()
pickle.dump(initial_time_stamp, open("initial_time_stamp.dat", "wb"))

for ii in range(num_tests):
    initial_time_stamp = pickle.load(open("initial_time_stamp.dat", "rb"))
    time_stamp = time.time()
    results = [measure_latency(host=i[1], port=80, runs=1) for i in ip_addresses]
    results = np.hstack((np.array([[time_stamp - initial_time_stamp]]), np.mean(np.array(results, dtype=np.float64), axis=1).reshape(1,-1)))
    delays_np[ii] = results
    # print("\n\n\n")
    print("Test #"+str(ii+1))
    # print(delays_np)
    pickle.dump(delays_np, open("delays.dat", "wb"))

# Reuse existing delays
# delays_np = pickle.load(open("delays.dat", "rb"))

for i in range(len(ip_addresses)):
    plt.plot(delays_np[:,0], delays_np[:,i+1], label=ip_addresses[i][0])

plt.legend()
plt.title("Delays")
plt.xlabel("Time (seconds)")
plt.ylabel("Delay (milliseconds)")
plt.show()