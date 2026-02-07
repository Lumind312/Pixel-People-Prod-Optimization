"""
	The problem:
		Given a number of people with specific jobs, and building that can employ specific jobs (including CPS and working time),
		find the configuration that will output the maximum amount of uninterrupted coins (no need to refresh).
		* Additional clause: if the building is full, the CPS will double.

	Approach:
		Class for each type of person
		Sort buildings ascending based on Multiplier
			Two building entries: one for x2, one for x1
			When sorting, sort by CPS, then x2, then time
		For each building, fill as much as possible
			For the x2, if we can't hit the cap number, don't add it and move on
			If we do hit the cap, remove it from later searches

"""

import sys
import pandas as pd
from ReadData import readFiles			# read in data using ../ReadData
from Class import Building, print_blist
from copy import deepcopy

test = ""
log = open('log.txt', 'w')

argc = len(sys.argv)
if argc > 1:
	test = "tests/" + sys.argv[1] + "/"
buildings,jobs,qbmap,qpmap = readFiles(test)
# print(buildings.to_string())
# print(jobs.to_string())
# print(qbmap)
# print(qpmap)
print("Buildings:", len(qbmap.keys()), "| People:", sum(qpmap.values()))

# changes blist
# inputs are a list of Building classes and a dict of (string : Job classes)
def get_prod(blist: list, pmap: dict):
	finished = set()
	# print(classListToStr(blist))
	# print(classListToStr(pmap))

	# 1. Check if we've already filled the full version
	# 2. Try to fill everything
	# 3. If full version, see if we actually filled everything
	# 4. Save filled building to "finished" list

	for i in range(len(blist)):		# i is current building index
		if blist[i].id in finished:
			blist[i] = 0		# nuke the building
			continue
		# get people who work there (based on buildings.csv)
		normal_name = blist[i].name
		if normal_name.find('_') != -1:
			normal_name = blist[i].name[:blist[i].name.find('_')]
		print(normal_name)

		workers = (buildings.loc[normal_name]["Worker1":"Worker6"]).to_list()

		# print(curr, workers)

		jobbing = []

		# make sure we actually have all of the jobs
		# hypothetically fill up the all of the people and check
		# if full, count the number of available
		for person in workers:
			if pd.notnull(person) and pmap[person] > 0:
				# print(curr, person, pmap[person])
				jobbing.append(person)
				pmap[person] -= 1
		log.write('[' + blist[i].name + ' (x' + str(blist[i].multiplier) + ')] Trying to add [' + ','.join(jobbing) + ']\n')
		
		if len(jobbing) == blist[i].cap or '_Full' not in blist[i].name:
			blist[i].set_workers(list(jobbing))
			finished.add(blist[i].id)
			log.write('  Added.\n')
		else:
			# undo removals
			for j in jobbing:
				pmap[j] += 1
			blist[i] = 0		# nuke the building
			log.write('  Could not add\n')


def find_config(qbmap: dict, qpmap: dict):
	# create buildings[] for sorting
	blist = []
	for i in qbmap:
		blist.append(Building(len(blist) // 2, buildings.loc[i], i, qbmap[i]))

		# x2
		blist.append(Building(len(blist) // 2, buildings.loc[i], i+'_Full', qbmap[i]))

		
	pmap = {}
	for i in qpmap:
		pmap[i] = qpmap[i]

	blist.sort(reverse=True)
	# print_blist(blist, simple=False)

	get_prod(blist, pmap)
	
	return blist, pmap

blist, pmap = find_config(qbmap, qpmap)

print_blist(blist, simple=False)

# readable in exe run
input("Finished running")
