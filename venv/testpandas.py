import pandas as pd
import numpy as np

print("hellopip")
l = [1,2,3,4,5]
print(np.sum(l))
availability = 99.99  # percent
total_time = 365 * 24  # hours in a year

downtime = (1 - availability / 100) * total_time
nines = (total_time - downtime) / total_time

print(f"Availability: {availability:.2f}%")
print(f"Number of nines: {nines:.0f}")