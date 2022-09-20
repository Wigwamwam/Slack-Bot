import pandas as pd
import random
import csv

data = pd.read_csv('quote.csv')
print(data.sample())
