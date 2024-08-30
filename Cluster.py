import copy
import pandas as pd
import time

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

# state = [int, {'Building': Building()}]
def printState(curr):
	print('\nState:')
	max = 0
	if type(curr[0]) is int:
		max = 1
		print(curr[0])

	for key in curr[0+max]:
		print(key, curr[0+max][key],end=', ')
	# print(curr[1+max])

# can do individual clusters of permutations
class Cluster:
	def __init__(self, buildings,jobs,qbmap,qpmap):
		self.buildings = buildings
		self.jobs = jobs
		self.qbmap = qbmap
		self.qpmap = qpmap
		
		self.max = [0, {}]
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
		ret = ret[:-2] + '}\n'
		
		# if len(self.max[2]) > 0:
		# 	ret += 'People: {'

		# 	# print people
		# 	people = copy.deepcopy(self.max[2])
		# 	for key in people:
		# 		ret += key + ' : ' + people[key] + ', '
		# 	ret = ret[:-2] + '}\n'
		
		return f"{ret}"

	class Building:
		# input: number of buildings
		def __init__(self, buildings, num):
			self.buildings = buildings
			self.jobs = [set() for i in range(int(num))]
		def __str__(self):
			return f"{self.jobs}"
		def __len__(self):
			return len(self.jobs)
		

		# input: job that we want to assign
		# returns True if success, False if fail
		# no need to error check since jobs will be selected by those whose workplace is here
		def insertJob(self, j: str) -> bool:
			for i in range(len(self.jobs)):
				if j not in self.jobs[i]:
					self.jobs[i].add(j)
					return True
			return False
		
		# input: job that we want to assign
		# returns True if success, False if fail
		def removeJob(self, j: str) -> bool:
			for i in range(len(self.jobs)-1, -1, -1):
				if j in self.jobs[i]:
					self.jobs[i].remove(j)
					return True
			return False
		
		def getCPS(self, name) -> int:
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

	# do the jobs that only have one workplace first, or if we have a one-to-one quantity
	# will automatically update self.max
	def filterEasy(self, builds, people):
		# preload the buildings with the no-brainer options
		# append the no-brainers to the phash at the end
		ez_people = {}		# dict for all no-brainers
		poplist = []
		for i in people:
			workplaces = self.jobs.loc[i[:-1]]['Workplace1':'Workplace3']
			if int(self.jobs.loc[i[:-1]]['Options']) == 1:
				ez_people[i] = workplaces[0]
				# self.max[2][i] = ez_people[i]
				
				builds[ez_people[i]].insertJob(i[:-1])
				self.max[1][ez_people[i]].insertJob(i[:-1])
				poplist.append(i)
				
		for i in poplist:
			people.pop(i)
		return ez_people
	
	# if qperson == qbuildings they can be assigned, do those
	def filterFit(self, builds, qpmap):
		# count = []
		poplist = []
		for i in qpmap:
			count = []
			workplaces = self.jobs.loc[i]['Workplace1':'Workplace3'].dropna().to_list()
			for w in workplaces:					# get the number of buildings (quantity) that this person can go to
				count.append(len(builds[w])) if w in builds else count.append(0)
			print(i, count)
			if sum(count) == qpmap[i]:
				for c in range(len(count)):
					if workplaces[c] in builds:
						while count[c] > 0:
							builds[workplaces[c]].insertJob(i)
							self.max[1][workplaces[c]].insertJob(i)
							count[c] -= 1
							qpmap[i] -= 1
				poplist.append(i)

		for i in poplist:
			qpmap.pop(i)
		# return ez_people

	def calcCPS(self, bdict) -> int:
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
				# self.max[2] = dict(curr[1])
			return
		
		# iterative step: set one of the jobs to a building, then recursively iterate through the rest
		
		workplaces = self.jobs.loc[plist[iter][:-1]]['Workplace1':'Workplace3'].dropna().to_list()
		# workplaces = [''] + workplaces				# assume every person will not have a place to go

		for w in workplaces:
			if not pd.isna(w):
			
				if w in blist and curr[0][w].insertJob(plist[iter][:-1]):			# add job to building. make sure assignment worked
					curr[1][plist[iter]] = w

				# printState(curr)
				
				# go to next level
				self.recursion(blist, plist, curr, iter+1, count)

				if w in blist:
					curr[0][w].removeJob(plist[iter][:-1])
					curr[1][plist[iter]] = ''


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

		qpmap = dict(self.qpmap)
		self.filterFit(builds, qpmap)

		people = {}
		for p in qpmap.keys():
			while qpmap[p] > 0:
				people[p+str(int(qpmap[p]))] = ''
				qpmap[p] -= 1

		ez_people = self.filterEasy(builds, people)		# filter the easy ones out

		# I'm just going to use dicts for people and buildings
		curr = [dict(builds),dict(people)]
		
		total = 1
		for i in people:
			num = float(self.jobs.loc[i[:-1]]['Options'])
			# num += 1.0				# +1 for empty
			total *= num
		print('Need to generate',total,'cases.')
		count = [0, total]				# show a load time
		# put it into recursion
		self.start_time = time.time()
		self.recursion(tuple(builds.keys()), tuple(people.keys()), curr, count=count)
		print('Finished recursion')
		print('Total time:', time.time()-self.start_time)

		# for i in ez_people:
		# 	self.max[2][i] = ez_people[i]

		# printState(self.max)
		self.done = True
		# input('.')

		return self.max