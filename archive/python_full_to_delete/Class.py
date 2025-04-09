# make a log file and save all of the steps to that instead of printing
log_file = open("log.txt","w")		# clear log.txt
log_file.close()
log_file = open("log.txt","a")

class Building:
	def __init__(self, id, info, full = True, time = 1):
		self.id = id

		self.cps = 0
		self.multiplier = int(info['Multiplier'][1:])
		self.maxCPS = int(info['MaxCPS'])
		self.workers = []
		self.name = info['Building name']
		self.full = full
		if full:
			self.multiplier *= 2
		self.totalOutput = self.maxCPS * time

	def __str__(self) -> str:
		return self.str() 
	def str(self) -> str:
		ans = self.name
		ans += ' (' + str(self.maxCPS) + ')'
		ans += ' ' + str(self.cps)
		ans += ' ' + str(self.workers)
		return ans

	# custom sorting for class
	def __lt__(self, other) -> bool:
		if self.maxCPS == other.maxCPS:
			if self.totalOutput == other.totalOutput:
				return self.name < other.name
			return self.totalOutput	< other.totalOutput
		return self.maxCPS < other.maxCPS

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
