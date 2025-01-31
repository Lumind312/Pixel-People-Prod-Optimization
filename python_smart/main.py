"""
	The problem:
		Given a number of people with specific jobs, and building that can employ specific jobs (including CPS and working time),
		find the configuration that will output the maximum amount of uninterrupted coins (no need to refresh).
		* Additional clause: if the building is full, the CPS will double. (WILL DO AFTER MAYBE)

	Approach:
		Class for each type of person
		Sort buildings ascending based on Multiplier
		For each building, first pull people that aren't attached to a job
		Then, if people are attached to a job, see if the resulting CPS creates an increase from the buildings we decrease
		If it works, then keep it
		If it doesn't work, test each person to see if we get an increase. Keep people who give an increase
"""

import sys
import pandas as pd
from Class import Job, Building
from Print import print_blist, print_pmap
from copy import deepcopy

test = ""

# input: prefix (if test, which one?)
def readCSVFiles(prefix=''):
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

	f = '../' + prefix + 'buildings.csv'
	b_df = pd.read_csv(f)
	b_df.set_index('Building name', inplace=True)
	if 'Lotsize' in b_df.columns:
		b_df.drop(columns=['Lotsize'], inplace=True)
	# https://stackoverflow.com/questions/26886653/create-new-column-based-on-values-from-other-columns-apply-a-function-of-multi
	if 'Capacity' not in b_df.columns:	
		b_df['Capacity'] = b_df.apply(cap, axis=1)

	j_df = 0
	'''
	f = '../' + prefix + 'jobs.csv'
	j_df = pd.read_csv(f)
	j_df.set_index('Profession', inplace=True)
	j_df['Options'] = j_df.apply(opt, axis=1)
	'''

	f = '../' + prefix + 'qbuilding.csv'
	qb_df = pd.read_csv(f, delimiter='\t')
	qb_df.set_index('Building name', inplace=True)
	if 'Template' in qb_df.index:
		qb_df.drop('Template', axis='index', inplace=True)
	if 'Time (mins)' not in qb_df.columns:
		qb_df['Time (mins)'] = 1
	qbmap = qb_df.to_dict()['Time (mins)']
	
	f = '../' + prefix + 'qpeople.csv'
	qp_df = pd.read_csv(f, delimiter='\t')
	qp_df.set_index('Profession', inplace=True)
	qpmap = qp_df.to_dict()['Quantity']

	return b_df, j_df, qbmap, qpmap

def classListToStr(cl) -> str:
	ret = '['
	for i in cl:
		if type(cl) == dict:
			ret += i + ': ' + cl[i].str()
		else:
			ret += i.str()
		ret += ', \n'
	ret = ret[:-3]
	ret += ']'
	return ret
def classListToCSV(cl, prefix='') -> None:
	with open(prefix+'result.csv', 'w') as f:
		f.write('Building name,CPS,Worker1,Worker2,Worker3,Worker4,Worker5,Worker6\n')
		for i in cl:
			f.write(i.name + ',' + str(i.cps))
			for w in range(len(i.workers)):
				f.write(',')
				if w < len(i.workers):
					f.write(i.workers[w])
			f.write('\n')



argc = len(sys.argv)
if argc > 1:
	test = "tests/" + sys.argv[1] + "/"
buildings,jobs,qbmap,qpmap = readCSVFiles(test)
# print(buildings.to_string())
# print(jobs.to_string())
# print(qbmap)
# print(qpmap)
print("Buildings:", len(qbmap.keys()), "| People:", sum(qpmap.values()))

# changes blist
# inputs are a list of Building classes and a dict of (string : Job classes)
def get_prod(blist, pmap):
	bref = {'' : -1}
	for i in range(len(blist)):
		bref[blist[i].name] = i
	# print(classListToStr(blist))
	# print(classListToStr(pmap))


	for i in range(len(blist)):		# i is current building index
		curr = blist[i].name		# name of current building
		while curr[-1].isdigit():
			curr = curr[:-1]

		# get people who work there (based on buildings.csv)
		if (curr != blist[i-1].name):
			workers = (buildings.loc[curr]["Worker1":"Worker6"]).to_list()

		# print(curr, workers)

		inc = 0					# keep track of increase/decrease when testing CPS
		count = 0

		# for each person, if they don't currently have a job, assign them

		# make sure we actually have all of the jobs
		# hypothetically fill up the all of the people and check if there is an increase
		buildRemove = []
		for person in workers:
			if pd.notnull(person) and person in pmap:
				# print(curr, person, pmap[person])
				prevJob = pmap[person].getJob()
				build = bref[prevJob]		# guaranteed to have person in pmap and guaranteed to have a job
				if build >= 0:				# if a prevJob exists, calculate removing it
					if blist[build].cps == int(buildings.loc[prevJob]["MaxCPS"]) and build not in buildRemove:
						inc -= (blist[build].cps // 2 + blist[build].multiplier)
					else:
						inc -= blist[build].multiplier
					buildRemove.append(build)
				count += 1
				inc += blist[i].multiplier + blist[i].multiplier

		# will be multiplier if we are not using full, 2x multiplier if we are using full
		# print(inc, 'Use full?', (count == int(buildings.loc[curr]["Capacity"]) and inc > 0))
		add = blist[i].multiplier + blist[i].multiplier * (int(count == int(buildings.loc[curr]["Capacity"]) and inc > 0))
		
		# if there is an increase, actually go through with the operation
		# if there is not an increase
		# for each person, see if there is an increase
		for person in workers:
			if pd.notnull(person) and person in pmap and person not in blist[i].workers:
				prevJob = pmap[person].getJob()		# gets min multiplier
				build = bref[prevJob]		# guaranteed to have person in pmap and guaranteed to have a job
				# print(person, pmap[person], blist[build])

				# check what the possible decrease would be
				if build >= 0:
					if blist[build].cps == int(buildings.loc[prevJob]["MaxCPS"]):		# if the prevJob had a full building, divide by 2 first
						dec = (blist[build].cps // 2 + blist[build].multiplier)
					else:
						dec = blist[build].multiplier

				# accept the change if the building should be full or we get a positive change in CPS
				if prevJob == '' or (count == int(buildings.loc[curr]["Capacity"]) and inc > 0) or (blist[i].multiplier >= dec and not blist[i] < blist[build]):
					# if we are removing from a building, decrement
					if build >= 0:
						if not blist[build].remove(person):
							print('ERROR: building.remove() failed at', blist[build].name, ':', person)
							exit(1)
						if blist[build].full():			# decrease multiplier if taking away from full
							for w in blist[build].workers:
								pmap[w].update(blist[build].multiplier, blist[build].name)
					
					pmap[person].assignJob([add, blist[i].maxCPS, curr])		# replaces min mulitplier for new one
					if not blist[i].add(person):
						print('ERROR: building.add() failed at', blist[i].name, ':', person)
						exit(1)
					
					if blist[i].full():
						for w in blist[i].workers:
							pmap[w].update(blist[i].maxCPS//2+blist[i].multiplier, curr)
		# dummy = input(classListToStr(blist) + '\n')

	# who's not assigned a building?
	# for i in pmap.values():
	# 	if [0, 0, ''] in i.buildings_list:
	# 		print("Empty:", i.name)

	print()
	# print(classListToStr(blist))
	# classListToCSV(blist)
	total = 0
	for i in range(len(blist)):
		total += blist[i].cps
	return total

def find_config(qbmap: dict, qpmap: dict, desc=False):
	# create buildings[] for sorting
	blist = []
	for i in qbmap:
		blist.append(Building(buildings.loc[i], i, qbmap[i]))									# time used here
		blist[-1].totalOutput = blist[-1].maxCPS * qbmap[i]		# x60 for seconds not needed

		
	pmap = {}
	for i in qpmap:
		if qpmap[i] > 0:
			pmap[i] = Job(qpmap[i], i)

	blist.sort(reverse=desc)	# the other is descending


	get_prod(blist, pmap)
	if desc:
		blist.reverse()
	
	# print_blist(blist)
	# print_pmap(pmap)

	return blist, pmap

# find the difference between the two lists
# need to fill in time into remainder
def get_diff(blist_asc: list, blist_des: list, show=False):

	# blist and blist2 are sorted, both ascending
	# print the buildings that have differences
	diff = []			# indices based on blist_asc
	blist_same = []
	if show:
		print("Asc | Dec")
	for i in range(len(blist_asc)):
		if blist_asc[i].name != blist_des[i].name:
			print("ERROR: lists are not in the same order")
			exit(1)
		
		w1 = list(blist_asc[i].workers)
		w2 = list(blist_des[i].workers)
		w1.sort()
		w2.sort()
		if w1 != w2:
			diff.append((i, blist_asc[i].cps - blist_des[i].cps))
			if show:
				print(blist_asc[i].name, blist_asc[i].cps, '|', blist_des[i].name, blist_des[i].cps, '|', blist_asc[i].cps - blist_des[i].cps)
		else:
			blist_same.append(blist_asc[i])
	diff = sorted(diff, key=lambda x: abs(x[1]), reverse=True)

	# diff has it listed as (diff_val, the blist index)
	if show:
		print(diff)

	# using the indices, get a dict of the buildings
	diff_ind = [x[0] for x in diff]
	remainder = []
	qpmap_rem = {}
	for i in diff_ind:
		remainder.append(Building(buildings.loc[blist_asc[i].name], blist_asc[i].name, qbmap[blist_asc[i].name]))	# time used here
		for w in blist_asc[i].workers:
			if w not in qpmap_rem:
				qpmap_rem[w] = 0
			qpmap_rem[w] += 1

	pmap_rem = {}
	for i in qpmap_rem:
		if qpmap_rem[i] > 0:
			pmap_rem[i] = Job(qpmap_rem[i], i)
	return blist_same, remainder, pmap_rem


blist_asc, pmap_asc = find_config(qbmap, qpmap)
blist_des, pmap_des = find_config(qbmap, qpmap, desc=True)

blist_final = []
while 1:
	# remainder is unpopulated buildings, blist_same is populated
	blist_same, remainder, pmap_rem = get_diff(blist_asc, blist_des, show=True)
	print("Same size:", len(blist_same), "| Rem size:", len(remainder), "| People:", len(pmap_rem.keys()))
	blist_final += list(blist_same)			# add blist_same to final
	if len(remainder) < 1:		# if we don't have any more diffs, break
		break

	blist_asc = deepcopy(remainder)
	pmap_asc = deepcopy(pmap_rem)
	get_prod(blist_asc, pmap_asc)
	
	blist_des = deepcopy(remainder)
	pmap_des = deepcopy(pmap_rem)
	get_prod(blist_des, pmap_des)

blist_final.sort(reverse=True)
print_blist(blist_final, simple=False)

# readable in exe run
print("Log written to file")
input("Finished running")
