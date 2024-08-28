"""
	The problem:
		Given a number of people with specific jobs, and building that can employ specific jobs (including CPS and working time),
		find the configuration that will output the maximum amount of uninterrupted coins (no need to refresh).
		* Additional clause: if the building is full, the CPS will double. (WILL DO AFTER MAYBE)

	Naive approach: Just put people into random allowed jobs and permutate until we get the right answer.
	Part 1: The No-Brainers
		First, we can sort the people who only have one job to go to. This includes for the buildings where we don't own other buildings they can go to.
		Second, if we have the number of people that can fill the number of buildings, put them all in.
			We can assume we don't have more people than the buildings available. (For now?)

	Then the real problem starts.
	Part 2: Marriage
		We now need to find some way to sort people into what fits best. In other words, find the/any configuration that'll work best.
"""

# read in buildings first. Can't put a person in a building that doesn't exist
# then read in people, throwing out those that don't have an existing place
# add the ones that are no-brainers first (one job or quantity == # of workplaces)

# deal with marriage


# --------------------------------------
import sys
import pandas as pd
import copy

test = ""

def cap(row):
	if not pd.isna(row['Worker6']):
		return 6
	if not pd.isna(row['Worker5']):
		return 5
	if not pd.isna(row['Worker4']):
		return 4
	if not pd.isna(row['Worker3']):
		return 3
	if not pd.isna(row['Worker2']):
		return 2
	# if not pd.isna(row['Worker1']):
	return 1
def opt(row):
	if not pd.isna(row['Workplace3']):
		return 3
	if not pd.isna(row['Workplace2']):
		return 2
	# if not pd.isna(row['Workplace3']):
	return 1

# input: prefix (if test, which one?)
def readCSVFiles(prefix=''):
	f = prefix + 'buildings.csv'
	b_df = pd.read_csv(f)
	b_df.set_index('Building name', inplace=True)
	b_df.drop(columns=['Lotsize'], inplace=True)
	# https://stackoverflow.com/questions/26886653/create-new-column-based-on-values-from-other-columns-apply-a-function-of-multi
	b_df['Capacity'] = b_df.apply(cap, axis=1)

	f = prefix + 'jobs.csv'
	j_df = pd.read_csv(f)
	j_df.set_index('Profession', inplace=True)
	j_df['Options'] = j_df.apply(opt, axis=1)

	f = prefix + 'qbuilding.csv'
	qb_df = pd.read_csv(f)
	qb_df.set_index('Building name', inplace=True)
	qbmap = qb_df.to_dict()['Quantity']

	f = prefix + 'qpeople.csv'
	qp_df = pd.read_csv(f)
	qp_df.set_index('Profession', inplace=True)
	qpmap = qp_df.to_dict()['Quantity']

	return b_df, j_df, qbmap, qpmap

def generateClusters(buildings):		# jobs df not needed
	# filter through data to get clusters to work on individually rather than as a whole
	# just do it on the whole thing
	sets = []

	for b in buildings.index:
		curr = {b}
		for p in buildings.loc[b]['Worker1':'Worker6']:
			if not pd.isna(p):
				curr.add(p)
		existsIn = []
		for i in range(len(sets)):
			for s in curr:
				if s in sets[i] and i not in existsIn:
					existsIn.append(i)					# duplicate indices are NOT fine
		
		# print(len(sets), existsIn)
		while len(existsIn) > 0:
			curr = curr.union(sets[existsIn[-1]])				# must be added/removed from the back to keep sets[] indices intact
			sets.remove(sets[existsIn[-1]])
			existsIn.pop()
		sets.append(curr)

	sets = sorted(sets, key=lambda x: len(x))
	# print(sets)
	return sets

# state = [{'Building': Building()}, [int]]
def printState(curr):
	print('\nState:')
	max = 0
	if type(curr[0]) is int:
		max = 1
		print(curr[0])

	for key in curr[0+max]:
		print(key, curr[0+max][key],end=', ')
	print(curr[1+max])

# can do individual clusters of permutations
class Cluster:
	def __init__(self, buildings,jobs,qbmap,qpmap):
		self.buildings = buildings
		self.jobs = jobs
		self.qbmap = qbmap
		self.qpmap = qpmap
		
		self.max = [0, {}, {}]
		self.done = False

		# print(self.qbmap, self.qpmap)
	def __str__(self):
		if not self.done:
			self.getMax()
		# print value
		ret = 'Val ' + str(self.max[0]) + '\nBuildings: {'
		
		# print buildings
		buildings = copy.deepcopy(self.max[1])
		reversed(buildings)
		for key in buildings:
			ret += key + ' : ' + str(buildings[key]) + ', '
		ret = ret[:-2] + '}\nPeople: {'

		# print people
		people = copy.deepcopy(self.max[2])
		for key in people:
			ret += key + ' : ' + people[key] + ', '
		ret = ret[:-2] + '}\n'
		
		return f"{ret}"

	class Building:
		# input: number of buildings
		def __init__(self, buildings, num):
			self.buildings = buildings
			self.jobs = [set() for i in range(int(num))]
		def __str__(self):
			return f"{self.jobs}"
		def len(self):
			return len(self.jobs)
		

		# input: job that we want to assign
		# returns True if success, False if fail
		# no need to error check since jobs will be selected by those whose workplace is here
		def insertJob(self, j):
			for i in range(len(self.jobs)):
				if j[:-1] not in self.jobs[i]:
					self.jobs[i].add(j[:-1])
					return True
			return False
		
		# input: job that we want to assign
		# returns True if success, False if fail
		def removeJob(self, j):
			for i in range(len(self.jobs)-1, -1, -1):
				if j[:-1] in self.jobs[i]:
					self.jobs[i].remove(j[:-1])
					return True
			return False
		
		def getCPS(self, name):
			sum = 0
			for i in self.jobs:
				# print(name, i)
				# print(buildings.loc[name])

				if len(i) < int(self.buildings.loc[name]['Capacity']):
					sum += len(i) * int(self.buildings.loc[name]['Multiplier'][1])
				elif len(i) > int(self.buildings.loc[name]['Capacity']):
					print("Error: more jobs than capacity allowed at:", name)
					exit(1)
				else:
					sum += int(self.buildings.loc[name]['MaxCPS'])
			return sum

	def calcCPS(self, bdict):
		sum = 0
		for i in bdict:
			sum += bdict[i].getCPS(i)
		return sum

	# iterate through keys and get a value to save
	def recursion(self, blist, plist, curr, iter=0, count=[0,0]):
		# print('Function begin:')
		# base case: we have reached the end of the people
		if iter == len(plist):
			count[0] += 1
			if count[0] % 1000 == 0 or count[0] == count[1]:
				print('Generated', count[0], 'of', count[1], 'permutations')
			
			val = self.calcCPS(curr[0])
			if val > self.max[0]:
				self.max[0] = val
				self.max[1] = copy.deepcopy(curr[0])
				self.max[2] = dict(curr[1])
			return
		
		# iterative step: set one of the jobs to a building, then recursively iterate through the rest
		
		workplaces = self.jobs.loc[plist[iter][:-1]]['Workplace1':'Workplace3'].dropna().to_list()
		workplaces = [''] + workplaces				# assume every person will have a place to go

		for w in workplaces:
			if not pd.isna(w):
			
				if w in blist and curr[0][w].insertJob(plist[iter]):			# add job to building. make sure assignment worked
					curr[1][plist[iter]] = w

				# printState(curr)
				
				# go to next level
				self.recursion(blist, plist, curr, iter+1, count)

				if w in blist:
					curr[0][w].removeJob(plist[iter])
					curr[1][plist[iter]] = ''

	# do the jobs that only have one workplace first
	# will automatically update self.max
	def filterEasy(self, builds, people):
		# preload the buildings with the no-brainer options
		# append the no-brainers to the phash at the end
		ez_people = {}		# dict for all no-brainers
		poplist = []
		for i in people:
			if int(self.jobs.loc[i[:-1]]['Options']) == 1:
				ez_people[i] = self.jobs.loc[i[:-1]]['Workplace1']
				self.max[2][i] = ez_people[i]
				
				builds[ez_people[i]].insertJob(i)
				self.max[1][ez_people[i]].insertJob(i)
				poplist.append(i)
		for i in poplist:
			people.pop(i)
		return ez_people
	
	# input: building_data, job_data, building_quantity, people_quantity
	def getMax(self):
		if self.done:
			return self.max
		
		# set up data
		builds = {}
		for b in self.qbmap.keys():
			temp = self.Building(self.buildings, self.qbmap[b])
			builds[b] = temp
		self.max[1] = copy.deepcopy(builds)

		people = {}
		for p in self.qpmap.keys():
			while self.qpmap[p] > 0:
				people[p+str(int(self.qpmap[p]))] = ''
				self.qpmap[p] -= 1

		ez_people = self.filterEasy(builds, people)		# filter the easy ones out

		# I'm just going to use dicts for people and buildings
		curr = [dict(builds),dict(people)]
		
		total = 1
		for i in people:
			total *= float(self.jobs.loc[i[:-1]]['Options'] + 1)			# +1 for empty
		print('Need to generate',total,'cases.')
		count = [0, total]				# show a load time
		# put it into recursion
		self.recursion(tuple(builds.keys()), tuple(people.keys()), curr, count=count)
		print('Finished recursion')

		for i in ez_people:
			self.max[2][i] = ez_people[i]

		# printState(self.max)
		self.done = True
		# input('.')

		return self.max

argc = len(sys.argv)
if argc > 1:
	test = "tests/" + sys.argv[1] + "/"
# queue, buildings = getQueue()
buildings,jobs,qbmap,qpmap = readCSVFiles(test)
# print(buildings.to_string())
# print(jobs.to_string())
# print(qbmap)
# print(qpmap)

clusters = generateClusters(buildings)
# print(clusters)

while {} in clusters:
	clusters.remove({})
for i in clusters:
	bdict = {}
	pdict = {}
	for x in i:
		if x in qbmap.keys():
			bdict[x] = qbmap[x]
		if x in qpmap.keys():
			pdict[x] = qpmap[x]

	
	# print('Make cluster with:\n', bdict, pdict)
	print('bdict_size', len(bdict), 'pdict_size', len(pdict))

	if len(bdict) < 1 or len(pdict) < 1:
		pass
		# print('Will not calculate empty sets')
	else:
		c = Cluster(buildings, jobs, bdict, pdict)
		c.getMax()
		print('This cluster results in:\n', c, '\n', end='')

# TODO: find a way to decrease the needed results by a LOT
# attempt: dp so we don't need to recalculate?
# or we can start stacking jobs back to normal (only one key per job type)