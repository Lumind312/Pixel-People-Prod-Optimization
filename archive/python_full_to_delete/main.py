import sys
import pandas as pd
from ReadData import readFiles			# read in data using ../ReadData
from Class import Building
from copy import deepcopy

test = ""

# 1. Create a list of buildings, one for non-filled, and one for filled
# 2. Load JobManager with quantity of people
# 3. Sort buildings
# 4. From largest to smallest:
#	If the building is marked as full, see if we have everyone we need. If we do, fill it
#	If the building is normal, fill as much as possible
#	Remove all people used from the JobManager



argc = len(sys.argv)
if argc > 1:
	test = "tests/" + sys.argv[1] + "/"
buildings,jobs,qbmap,qpmap = readFiles(test)
# print(buildings.to_string())
# print(jobs.to_string())
# print(qbmap)
# print(qpmap)
print("Buildings:", len(qbmap.keys()), "| People:", sum(qpmap.values()))


# create list of buildings
blist = []
for i in qbmap.items():
	print(i)
	# for now, assume we only have one of each building
	blist.append(Building(0, i[0], buildings.loc[i[0]], i[1], True))	# default id for now
	blist.append(Building(0, i[0], buildings.loc[i[0]], i[1], False))	# one building will be as if it's not filled
	blist[-1].maxCPS /= 2
	

# sort ascending
blist.sort()
print(blist)