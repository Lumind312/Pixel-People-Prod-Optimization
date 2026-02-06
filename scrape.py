import requests
from bs4 import BeautifulSoup
import pandas as pd

# given a link to a page, scrape it for a row of info
def getDataFromPage(link):
	r = requests.get(link)
	print(r, link)
	
	soup = BeautifulSoup(r.content, 'html.parser')
	f = open('temp_page.html', 'w', encoding='utf-8')		# just to see what we are scraping from
	f.write(str(soup))
	f.close()

	s = soup.find('table', class_='wikia-infobox').find('tbody').find_all('tr')
	data = {}

	for i in s:
		if i.find('td') != None and i.find('th') != None:
			title = i.find('th').get_text().strip()
			if title == 'Professions':
				data['Workers'] = i.find('td').get_text().strip().split(',')
				data['Workers'] = [i.strip() for i in data['Workers']]
				if '' in data['Workers']:
					data['Workers'].remove('')
				# print(data['Building name'], data['Workers'])
			elif title == 'Production multiplier':
				data['Multiplier'] = 'x' + i.find('td').get_text().strip()[1:]
		elif i.find('th', class_='wikia-infobox-header') != None:
			data['Building name'] = i.find('th', class_='wikia-infobox-header').get_text().strip()

	# print(data)

	# manual fixes
	if data['Building name'] == 'Rail Terminal':
		data['Building name'] = 'Railroad Station'

	if data['Building name'] == 'Laboratory':
		data['Workers'] = ['Monster','Mad Scientist','Henchman']
	if data['Building name'] == 'Secret Hideout':
		data['Workers'] = ['Monster Hunter','Lawn Gnome']
	if data['Building name'] == 'Funeral Parlor':
		data['Workers'] = ['Coroner','Gravedigger','Landscaper']

	# capacity
	data['Capacity'] = len(data['Workers'])						# capacity
	data['MaxCPS'] = data['Capacity'] * int(data['Multiplier'][1:]) * 2	# maxcps

	# put workers in individual slots
	for i in range(0,6):
		if i >= len(data['Workers']):
			data['Worker' + str(i+1)] = pd.NA
		else:
			data['Worker' + str(i+1)] = data['Workers'][i].strip()
	
	data.pop('Workers')	

	# print(data)
	return data

def getLinks(table_link):
	# soup reading
	r = requests.get(table_link)
	print(r, table_link)
	
	soup = BeautifulSoup(r.content, 'html.parser')
	f = open('temp.html', 'w', encoding='utf-8')		# just to see what we are scraping from
	f.write(str(soup))
	f.close()

	# find the big table
	s = soup.find('table').find('tbody').find_all('tr')
	
	df = pd.DataFrame(columns=['Building name','MaxCPS','Multiplier','Worker1','Worker2','Worker3','Worker4','Worker5','Worker6','Capacity'])
	for i in s:
		link = i.find('a')
		if link != None:
			link = 'https://pixelpeople.fandom.com' + i.find('a')['href']
			df = df._append(getDataFromPage(link), ignore_index=True)

	# print(df)
	return df

# use BeautifulSoup to read in the data
# table size is the table width
# target_columns holds the indices of the columns we want to read in
def readPage(link, table_size, target_columns):
	# soup reading
	r = requests.get(link)
	print(r, link)
	
	soup = BeautifulSoup(r.content, 'html.parser')
	f = open('temp.html', 'w', encoding='utf-8')		# just to see what we are scraping from
	f.write(str(soup))
	f.close()

	# find the big table
	s = soup.find('table', class_='wikitable sortable')
	header = s.find('tbody').find('tr').find_all('th')			# column titles
	content = s.find_all('td')									# the rest of the data
	# print(content)

	data = []
	# save the header names, because they're in a different html element
	for i in range(len(header)):
		if i % table_size == 0:
			data.append([header[i].get_text().strip()])			# name
		for tc in target_columns:								# I specify which columns we are grabbing
			if i % table_size == int(tc):
				x = header[i].get_text()[:-1]
				data[-1].append(x)

	# save the values
	for i in range(len(content)):
		if i % table_size == 0:
			data.append([content[i].get_text().strip()])			# name
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


jobs = pd.DataFrame(readPage('https://pixelpeople.fandom.com/wiki/Professions', 5, [4]))
formatDF(jobs)

f = open('jobs.csv', 'w')
f.write(jobs.to_csv(index=False, header=True, lineterminator='\n'))
f.close()

# df = pd.DataFrame(readPage('https://pixelpeople.fandom.com/wiki/List:Buildings', 8, [1,2,3,7]))
# formatDF(df)

# f = open('buildings.csv', 'w')
# f.write(df.to_csv(index=False, header=True, lineterminator='\n'))
# f.close()

# some entries on the table have incorrect values, so I guess we're just going to scrape and look at every single item  >:(
df = getLinks('https://pixelpeople.fandom.com/wiki/List:Buildings')

f = open('buildings.csv', 'w')
f.write(df.to_csv(index=False, header=True, lineterminator='\n'))
f.close()