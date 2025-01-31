import pandas as pd

# read in expected result
exp = pd.read_csv('result.csv')
exp.set_index('Building name', inplace=True)
exp.drop(columns=['Worker1','Worker2','Worker3','Worker4','Worker5','Worker6'], inplace=True)

# read in actual result
act = pd.read_csv('reference.txt', delimiter='\t')
act.set_index('Building name', inplace=True)
act.drop(columns=['IncrPerCost'], inplace=True)

# so we can see maxCPS
build_df = pd.read_csv('buildings.csv')
build_df = build_df.set_index('Building name')['MaxCPS']

j = exp.join(build_df)
j = j.join(act)

# print(j)

diff = j[j['CPS'] != j['Curr CPS']]
print(diff.loc[:, ['MaxCPS','CPS','Curr CPS']])

print(sum(j['CPS']), sum(j['Curr CPS']))