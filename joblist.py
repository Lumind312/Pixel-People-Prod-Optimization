import pandas

df = pandas.read_csv('jobs.csv')
lst = df['Profession'].to_list()
'\n'.join(lst)
for i in range(len(lst)):
	lst[i] += ',1'

f = open('temp.txt', 'w')
f.write('\n'.join(lst))
f.close()