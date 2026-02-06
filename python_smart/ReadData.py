import pandas as pd

# input: prefix (if test, which one?)
def readFiles(prefix=''):
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