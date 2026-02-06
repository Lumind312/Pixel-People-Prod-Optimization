class Job:
	# buildings_list = []
	# remaining = 0		# how many people we have left
	# name = ''			# irrelevant. used for print

	def __init__(self, num=0, name = ''):
		# self.buildings_list = [[0,0,'']] * num
		self.remaining = num
		self.name = name

	def __str__(self):
		return self.str()
	
	def available(self) -> bool:
		return self.remaining > 0
	

class Building:
	# cps = 0
	# multiplier = 0
	# maxCPS = 0
	# workers = []
	# name = ''
	# time = 0

	# use "name_Full" to make it x2
	def __init__(self, id, info, name, time = 1):
		self.id = id

		self.cps = 0
		self.multiplier = int(info['Multiplier'][1:])
		self.maxCPS = int(info['MaxCPS'])
		self.workers = []
		self.name = name
		if '_Full' in self.name:
			self.multiplier *= 2
		self.cap = int(info['Capacity'])
		self.time = time

	def __str__(self) -> str:
		return self.str() 
	def str(self) -> str:
		ans = self.name
		ans += ' (' + str(self.maxCPS) + ',x' + str(self.multiplier) + ')'
		ans += ' ' + str(self.cps)
		ans += ' ' + str(self.workers)
		return ans
	
	# use for sorting
	FULL_OUTPUT = False
	def __lt__(self, other) -> bool:
		b1 = self
		b2 = other

		time1 = b1.time
		time2 = b2.time
		if not self.FULL_OUTPUT:
			time1 = 1
			time2 = 1

		# maxCPS, then multiplier, then time, then name

		if b1.maxCPS == b2.maxCPS:
			if b1.multiplier == b2.multiplier:
				if time1 == time2:
					return b1.name < b2.name
				return time1 < time2
			return b1.multiplier < b2.multiplier
		return b1.maxCPS < b2.maxCPS
	
	def set_workers(self, names) -> None:
		self.workers.append(names)
		self.cps = self.multiplier * len(self.workers)



# simple=False for full building print
def print_blist(blist, simple=True):
	total_sum = 0
	sums = {}
	for i in range(1, 9):
		for j in range(1, 7):
			sums[i*j * 2] = 0

	total_workers = 0
	for i in range(len(blist)):
		if blist[i] == 0:
			continue

		if not simple:
			print(blist[i].id, blist[i])

		total_sum += blist[i].cps
		# sums[blist[i].maxCPS] += blist[i].cps
		total_workers += len(blist[i].workers)

	print('\nBuildings:', len(blist), '| People:', total_workers)
	print("Final CPS:", total_sum)
	print()

def print_pmap(qpmap):
	for i in qpmap.keys():
		print(i, qpmap[i])