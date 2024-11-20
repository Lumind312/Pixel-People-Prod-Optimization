class Job:
	buildings_list = []
	min = 0
	name = ''			# irrelevant. used for print

	def __init__(self, num, name = ''):
		self.buildings_list = [[0,0,'']] * num
		self.name = name
		self.min = 0
	def __str__(self):
		return self.str()
	
	def getJob(self) -> str:
		return self.buildings_list[self.min][2]
	
	# list = [removable cps, maxCPS, building]
	def assignJob(self, l) -> None:
		print(self.name, 'reassigns', self.buildings_list[self.min], '->', end=' ')
		self.buildings_list[self.min] = l
		self.min = self.buildings_list.index(min(self.buildings_list))
		print(l)

	def update(self, n, build_name):
		# print(self.name, self.buildings_list)
		j = -1
		for i in range(len(self.buildings_list)):
			if build_name == self.buildings_list[i][2]:
				j = i

		if j < 0:
			print("ERROR:",build_name,"not found in job's list.", self, "ABORTING.")
			exit(1)
		self.buildings_list[j][0] = n
		self.min = self.buildings_list.index(min(self.buildings_list))
	
	# 
	def str(self) -> str:
		return str(self.buildings_list)

class Building:
	cps = 0
	multiplier = 0
	maxCPS = 0
	workers = []
	name = ''

	def __init__(self, info, name):
		self.cps = 0
		self.multiplier = int(info['Multiplier'][1:])
		self.maxCPS = int(info['MaxCPS'])
		self.workers = []
		self.name = name
		self.totalOutput = 1

	def __str__(self) -> str:
		return self.str() 
	def str(self) -> str:
		ans = self.name
		ans += ' (' + str(self.maxCPS) + ')'
		ans += ' ' + str(self.cps)
		ans += ' ' + str(self.workers)
		return ans

	def __lt__(self, other) -> bool:
		if self.maxCPS == other.maxCPS:
			if self.totalOutput == other.totalOutput:
				return self.name < other.name
			return self.totalOutput	< other.totalOutput
		return self.maxCPS < other.maxCPS

	def full(self):
		return self.cps == self.maxCPS
	def add(self, name) -> bool:
		if name in self.workers:
			return False
		before = self.cps

		self.workers.append(name)
		self.cps += self.multiplier
		if self.cps*2 == self.maxCPS:
			self.cps *= 2
		
		print(self.name, '(', self.maxCPS, ')', 'adds', name, '|', before, '->', self.cps)
		return True
	def remove(self, name) -> bool:
		if name not in self.workers:
			return False
		before = self.cps

		self.workers.remove(name)
		if self.cps == self.maxCPS:
			self.cps //= 2
		self.cps -= self.multiplier
		
		print(self.name, '(', self.maxCPS, ')', 'removes', name, 'from', self.workers, '|', before, '->', self.cps)
		return True