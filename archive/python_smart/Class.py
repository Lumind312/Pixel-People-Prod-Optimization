# make a log file and save all of the steps to that instead of printing
log_file = open("log.txt","w")		# clear log.txt
log_file.close()
log_file = open("log.txt","a")

class Job:
	buildings_list = []
	min = 0				# index for lowest CPS building assignment
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
		log_file.write(self.name + ' reassigns ' + str(self.buildings_list[self.min]) + ' -> ')
		self.buildings_list[self.min] = l
		self.min = self.buildings_list.index(min(self.buildings_list))
		log_file.write(str(l) + '\n')

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
	
	def str(self) -> str:
		return str(self.buildings_list)

class Building:
	cps = 0
	multiplier = 0
	maxCPS = 0
	workers = []
	name = ''
	totalOutput = 0

	def __init__(self, id, info, name, time = 1):
		self.id = id

		self.cps = 0
		self.multiplier = int(info['Multiplier'][1:])
		self.maxCPS = int(info['MaxCPS'])
		self.workers = []
		self.name = name
		self.totalOutput = self.maxCPS * time

	def __str__(self) -> str:
		return self.str() 
	def str(self) -> str:
		ans = self.name
		ans += ' (' + str(self.maxCPS) + ')'
		ans += ' ' + str(self.cps)
		ans += ' ' + str(self.workers)
		return ans

	# change this for sorting
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
		
		log_file.write(self.name + ' ( ' + str(self.maxCPS) + ' ) adds ' + name + ' | ' + str(before) + ' -> ' + str(self.cps) + '\n')
		return True
	def remove(self, name) -> bool:
		if name not in self.workers:
			return False
		before = self.cps

		self.workers.remove(name)
		if self.cps == self.maxCPS:
			self.cps //= 2
		self.cps -= self.multiplier
		
		log_file.write(self.name + ' ( ' + str(self.maxCPS) + ' ) removes ' + name + ' from ' + str(self.workers) + ' | ' + str(before) + ' -> ' + str(self.cps) + '\n')
		return True