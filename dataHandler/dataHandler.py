import pandas as pd
import numpy as np

dataFile = pd.read_csv('data/testdata1.csv')
df = pd.DataFrame(dataFile)

print(df)