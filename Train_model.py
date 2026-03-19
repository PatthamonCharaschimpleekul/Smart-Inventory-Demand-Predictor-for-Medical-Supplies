import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df_daily = pd.read_csv('data/salesdaily.csv')
df_month = pd.read_csv('data/salesmonthly.csv')

print(df_daily.info())
print(df_month.info())
