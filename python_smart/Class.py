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

		# multiplier, then filled buildings, then time, then name
		if b1.multiplier == b2.multiplier:
			if ('_' in b1.name and '_' in b2.name) or ('_' not in b1.name and '_' not in b2.name):
					if time1 == time2:
						return b1.name < b2.name
					return time1 < time2
			return '_' in b2.name
		return b1.multiplier < b2.multiplier
	
	def set_workers(self, names) -> None:
		self.workers = list(names)
		self.cps = self.multiplier * len(self.workers)



# simple=False for full building print
def print_blist(blist: list, simple=True):
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
		sums[blist[i].maxCPS] += blist[i].cps
		total_workers += len(blist[i].workers)

	cps = []
	if not simple:
		for i in sums:
			if sums[i] > 0:
				cps.append((i, sums[i]))
	cps.sort(reverse=True)
	print('\n'.join([str(x[0]) + ' : ' + str(x[1]) for x in cps]))
	print('\nBuildings:', len(blist), '| People:', total_workers)
	print("Final CPS:", total_sum)
	print()
