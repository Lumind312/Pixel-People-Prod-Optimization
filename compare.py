import pandas as pd

# read in expected result
exp = pd.read_csv('result.csv')
exp.set_index('Building name', inplace=True)
exp.drop(columns=['Worker1','Worker2','Worker3','Worker4','Worker5','Worker6'], inplace=True)

# read in actual result
act = pd.read_csv('reference.txt', delimiter='\t')
act.set_index('Building name', inplace=True)
act.drop(columns=['IncrPerCost'], inplace=True)

j = exp.join(act)

# print(j)

diff = j[j['CPS'] != j['Curr CPS']]
print(diff)

print(sum(j['CPS']), sum(j['Curr CPS']))