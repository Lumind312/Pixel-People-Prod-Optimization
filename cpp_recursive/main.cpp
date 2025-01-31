// priority queue of buildings, in descending order of the most money (make it a function so I can change it out if needed)
// two building options: one with the double (x2) cps, and one with the single (x1) cps
// that way, we try the double first, then try the single if the double fails.
// for now, assume that we only have one of each building. I'll think of if we have 2 later down the line maybe

#include <bits/stdc++.h>
using namespace std;

#include "Prints.h"
#include "CSVReader.h"
#include "Cluster.h"

// const int MAX_WORKERS = 6;
// const int MAX_JOBS = 3;

int main(int argc, char* argv[]) {
	// ios_base::sync_with_stdio(false);
	// cin.tie(NULL);
	// cout.tie(NULL);

	string test;			// use test files by putting an argument in command line
	test = argc > 1 ? argv[1] : "";
	
	// read all of the data in
	CSVReader reader(test);
	auto buildings = reader.getDataframeFromCSV("../buildings.csv");
	auto jobs = reader.getDataframeFromCSV("../jobs.csv");
	auto qbmap = reader.getMapFromCSV("../qbuilding.csv");
	auto qpmap = reader.getMapFromCSV("../qpeople.csv");
	cout << "Read in data.\n";

	// make clusters based on data given
	vector<set<string>> clusters = generateClusters(buildings);
	cout << "Clusters:\n";
	for (unsigned i = 0; i < clusters.size(); i++) {
		cout << setToStr(clusters.at(i));
	}

	// finally, create qmaps of buildings and people, and use the clusters to generate the max value + config
	map<string, int> bdict, pdict;
	for (unsigned i = 0; i < clusters.size(); i++) {		// first one will always be mechanic, which has a cps of 0
		bdict.clear();
		pdict.clear();

		for (auto x: clusters.at(i)) {
			if (qbmap.find(x) != qbmap.end())
				bdict[x] = qbmap[x];
			if (qpmap.find(x) != qpmap.end())
				pdict[x] = qpmap[x];
		}
		if (bdict.size() < 1 || pdict.size() < 1) {
			continue;
		}

		// else
		if (pdict.size() < 100) {		// temporarily don't calculate the big one
		cout << "Make cluster with:\n";
		cout << "bdict_size: " << bdict.size() << " | pdict_size: "<< pdict.size() << endl;
		// printMap(bdict);
		// printMap(pdict);

		Cluster c = Cluster(&buildings, &jobs, bdict, pdict);
		cout << "Result:\n" << c.str() << endl;
		}
	}

	cout << "Run complete" << endl;

	return 0;
}
