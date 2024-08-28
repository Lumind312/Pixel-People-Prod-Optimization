import requests
from bs4 import BeautifulSoup
import pandas as pd

# use BeautifulSoup to read in the data
# table size is the table width
# target_columns holds the indices of the columns we want to read in
def readPage(link, table_size, target_columns):
	# soup reading
	r = requests.get(link)
	print(r, link)
	
	soup = BeautifulSoup(r.content, 'html.parser')
	f = open('temp.html', 'w', encoding='utf-8')
	f.write(str(soup))
	f.close()

	s = soup.find('table', class_='wikitable sortable')
	header = s.find('tbody').find('tr').find_all('th')			# column titles
	content = s.find_all('td')									# the rest of the data
	# print(content)

	data = []
	# save the header names, because they're in a different html element
	for i in range(len(header)):
		if i % table_size == 0:
			data.append([header[i].get_text()[:-1]])			# name
		for tc in target_columns:								# I specify which columns we are grabbing
			if i % table_size == int(tc):
				x = header[i].get_text()[:-1]
				data[-1].append(x)

	# save the values
	for i in range(len(content)):
		if i % table_size == 0:
			data.append([content[i].get_text()[:-1]])			# name
		for tc in target_columns:								# I specify which columns we are grabbing
			if i % table_size == int(tc):
				x = content[i].get_text()[:-1].split(',')		# split() numerous workers/workplaces
				for j in x:
					data[-1].append(j.strip())
	# print(data)

	return data

# change the column names to first row
def formatDF(df):
	header = df.iloc[0].to_list()
	# print(header)
	num = 1
	# basically rename the end columns to 'Worker1','Worker2', etc.
	for i in range(1, len(header)):
		if header[i-1].find('Work') != -1:
			header[i-1] = header[i-1][:-1] + str(num)
			num += 1
			header[i] = header[i-1][:-1] + str(num)

	df.columns = header
	df.drop(inplace=True, index=0)
	
	# print(df)


df = pd.DataFrame(readPage('https://pixelpeople.fandom.com/wiki/Professions', 5, [4]))
formatDF(df)

f = open('jobs.csv', 'w')
f.write(df.to_csv(index=False, header=True, lineterminator='\n'))
f.close()

df = pd.DataFrame(readPage('https://pixelpeople.fandom.com/wiki/List:Buildings', 8, [1,2,3,7]))
formatDF(df)

f = open('buildings.csv', 'w')
f.write(df.to_csv(index=False, header=True, lineterminator='\n'))
f.close()
