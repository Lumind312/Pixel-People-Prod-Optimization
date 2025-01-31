from Class import Job, Building

# simple=False for full building print
def print_blist(blist, simple=True):
	total_sum = 0
	sums = {4: 0, 6: 0, 8: 0, 10: 0, 12: 0, 16: 0, 18: 0, 20: 0, 24: 0, 30: 0, 32: 0, 36: 0, 40: 0, 96: 0}

	total_workers = 0
	curr = 0
	for i in range(len(blist)):
		if not simple:
			print(i, blist[i])
		sums[blist[i].maxCPS] += blist[i].cps
		total_sum += blist[i].cps
		curr += blist[i].cps
		total_workers += len(blist[i].workers)

	for i in sums:
		print(i, sums[i])
	print('Buildings:', len(blist), 'People:', total_workers)
	print("Final CPS:", total_sum)
	print()

def print_pmap(qpmap):
	for i in qpmap.keys():
		print(i, qpmap[i])