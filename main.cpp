// priority queue of buildings, in descending order of the most money (make it a function so I can change it out if needed)
// two building options: one with the double (x2) cps, and one with the single (x1) cps
// that way, we try the double first, then try the single if the double fails.
// for now, assume that we only have one of each building. I'll think of if we have 2 later down the line maybe

#include <bits/stdc++.h>
using namespace std;

#include "CSVReader.h"
// #include "Cluster.h"

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
	auto buildings = reader.getDataframeFromCSV("buildings.csv");
	auto jobs = reader.getDataframeFromCSV("jobs.csv");
	auto qbmap = reader.getMapFromCSV("qbuilding.csv");
	auto qpmap = reader.getMapFromCSV("qpeople.csv");


	return 0;
}
