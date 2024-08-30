"""
	The problem:
		Given a number of people with specific jobs, and building that can employ specific jobs (including CPS and working time),
		find the configuration that will output the maximum amount of uninterrupted coins (no need to refresh).
		* Additional clause: if the building is full, the CPS will double. (WILL DO AFTER MAYBE)

	Naive approach: Just put people into random allowed jobs and permutate until we get the right answer.
	Part 1: The No-Brainers
		First, we can sort the people who only have one job to go to. This includes for the buildings where we don't own other buildings they can go to.
		Second, if we have the number of people that can fill the number of buildings, put them all in.
			We can assume we don't have more people than the buildings available. (For now?)

	Then the real problem starts.
	Part 2: Marriage
		We now need to find some way to sort people into what fits best. In other words, find the/any configuration that'll work best.
"""

# read in buildings first. Can't put a person in a building that doesn't exist
# then read in people, throwing out those that don't have an existing place
# add the ones that are no-brainers first (one job or quantity == # of workplaces)

# deal with marriage


# --------------------------------------
import sys
import pandas as pd
import Cluster

test = ""

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

# input: prefix (if test, which one?)
def readCSVFiles(prefix=''):
	f = prefix + 'buildings.csv'
	b_df = pd.read_csv(f)
	b_df.set_index('Building name', inplace=True)
	b_df.drop(columns=['Lotsize'], inplace=True)
	# https://stackoverflow.com/questions/26886653/create-new-column-based-on-values-from-other-columns-apply-a-function-of-multi
	b_df['Capacity'] = b_df.apply(cap, axis=1)

	f = prefix + 'jobs.csv'
	j_df = pd.read_csv(f)
	j_df.set_index('Profession', inplace=True)
	j_df['Options'] = j_df.apply(opt, axis=1)

	f = prefix + 'qbuilding.csv'
	qb_df = pd.read_csv(f)
	qb_df.set_index('Building name', inplace=True)
	qbmap = qb_df.to_dict()['Quantity']

	f = prefix + 'qpeople.csv'
	qp_df = pd.read_csv(f)
	qp_df.set_index('Profession', inplace=True)
	qpmap = qp_df.to_dict()['Quantity']

	return b_df, j_df, qbmap, qpmap



argc = len(sys.argv)
if argc > 1:
	test = "tests/" + sys.argv[1] + "/"
# queue, buildings = getQueue()
buildings,jobs,qbmap,qpmap = readCSVFiles(test)
# print(buildings.to_string())
# print(jobs.to_string())
# print(qbmap)
# print(qpmap)

clusters = Cluster.generateClusters(buildings)
# print(clusters)

while {} in clusters:
	clusters.remove({})
for i in clusters:
	bdict = {}
	pdict = {}
	for x in i:
		if x in qbmap.keys():
			bdict[x] = qbmap[x]
		if x in qpmap.keys():
			pdict[x] = qpmap[x]

	
	# print('Make cluster with:\n', bdict, pdict)
	print('bdict_size', len(bdict), 'pdict_size', len(pdict))

	if len(bdict) < 1 or len(pdict) < 1:
		pass
		# print('Will not calculate empty sets')
	else:
		c = Cluster.Cluster(buildings, jobs, bdict, pdict)
		c.getMax()
		print('This cluster results in:\n', c, '\n', end='')

# TODO: find a way to decrease the needed results by a LOT