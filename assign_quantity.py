# get web-scraped files, add from quantity files
import pandas as pd

df = pd.read_csv('qbuilding.csv')
df.fillna(1.0,inplace=True)
print(df)

f = open('qbuilding.csv', 'w')
f.write(df.to_csv(index=False, header=True, lineterminator='\n'))
f.close()