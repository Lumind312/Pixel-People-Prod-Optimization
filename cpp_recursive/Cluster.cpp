#include "Cluster.h"
#include <bits/stdc++.h>
#include "DF_Headers.h"
#include "Prints.h"
using namespace std;

// default constructor
// needed for default creation in builds map, but there are branches in functions (that return 0) just in case
Building::Building() {
	info = nullptr;
	name = "";
	maxCPS = 0;
	multiplier = 0;
	quantity = 1;
	// workers.clear()
	// fullCPS = false;
}

// input is address of the dataframe row and quantity
Building::Building(vector<string>* building, int num = 1) : info(building) {
	name = info->at(Name);
	maxCPS = stoi(info->at(MaxCPS));
	multiplier = stoi(info->at(Multiplier).substr(1));
	quantity = num;

	for (int i = Worker1; i <= Worker6 && !building->at(i).empty(); i++) {
		workers[building->at(i)] = 0;
	}
}

// print workers
// TODO: add CPS stuff
string Building::str() const {
	string ans = name;
	
	ans += " (" + to_string(this->maxCPS) + ") " + to_string(this->getCPS());
	ans += " : {";
	for (map<string, int>::const_iterator i = workers.cbegin(); i != workers.cend(); i++) {
		if (i != workers.cbegin())
			ans += ", ";
		ans += i->first + ": " + to_string(i->second);
	} ans += "}";
	return ans;
}

// true if job can and was added, false if not
bool Building::insertJob(const string& j) {
	if (info == nullptr)
		return false;

	if (workers.find(j) != workers.end() && workers[j] < quantity) {
		workers[j]++;
		return true;
	}

	return false;
}
// true if job exists and was removed, false if not
// go from the back of the list to make cps front-heavy
bool Building::removeJob(const string& j) {
	if (info == nullptr)
		return false;

	if (workers.find(j) != workers.end() && workers[j] > 0) {
		workers[j]--;
		return true;
	}
	return false;
}

// calculate all building CPS based on number of workers
int Building::getCPS() const {
	if (info == nullptr)
		return 0;
	
	int min = workers.begin()->second, total = 0;
	for (map<string, int>::const_iterator i = workers.cbegin(); i != workers.cend(); i++) {
		total += i->second;
		if (i->second < min)
			min = i->second;
	}

	return (total + min*workers.size()) * multiplier;
}

// -------------------

Cluster::Cluster(map<string, vector<string>> *buildings, map<string, vector<string>> *jobs, const map<string, int>& qbmap, const map<string, int>& qpmap) :
buildings(buildings), jobs(jobs), qbmap(qbmap), qpmap(qpmap) {
	maxVal = 0;
	done = false;
}

// print max and config
string Cluster::str() {
	if (!done) {
		getMax();
	}

	string ans = "Max: ";
	ans.append(to_string(getMax()));
	ans.push_back('\n');
	ans.append(configStr());
	ans.push_back('\n');

	return ans;
}

// assign the jobs that only have one workplace
// make changes to parameters
void Cluster::filterEasy(map<string, Building>& builds, vector<string>& people) {
	vector<string> newp;
	string currPerson;
	vector<string> currRow;
	for (unsigned i = 0; i < people.size(); i++) {
		currPerson = people.at(i);
		currRow = jobs->at(currPerson);
		cout << currPerson << endl;
		
		// needs to have only 1 workplace.
		// should have a spot guaranteed
		if (!(stoi(currRow.at(Options)) == 1 && builds[currRow.at(Workplace1)].insertJob(currPerson))) {
			newp.push_back(people.at(i));
		}
	}
	people = newp;
}
// assign jobs where we have a one-to-one quantity between the job and their buildings
// 	remove curr later
void Cluster::filterFit(map<string, Building>& builds, map<string,int>& qpmap) {
	int sum;
	vector<int>curr(3);
	vector<string> currRow;
	for (auto i: qpmap) {
		sum = 0;
		curr.resize(3,0);
		currRow = jobs->at(i.first);
		// get number of buildings
		for (unsigned j = 0; j < 3 && !currRow.at(j).empty(); j++) {
			if (builds.find(currRow.at(j+Workplace1)) != builds.end()) {
				curr.at(j) += builds[currRow.at(j+Workplace1)].quantity;
				sum += curr.at(j);
			}
		}

		// if the numbers match, put them in buildings and remove the job
		if (sum == i.second) {
			for (unsigned j = 0; j < 3 && !currRow.at(j).empty(); j++) {
				while (curr.at(j) > 0) {
					builds[currRow.at(j+Workplace1)].insertJob(i.first);
					curr.at(j)--;
				}
			}
			qpmap.erase(i.first);
		}
		curr.clear();
	}
}
// iterate through all of the buildings and get their CPS's
int Cluster::calcCPS(const map<string, Building>& bdict) const {
	int sum = 0;
	for (auto& i: bdict) {
		sum += i.second.getCPS();
	}
	return sum;
}
void printState(map<string, Building>& currBuilds) {
	cout << "State:\n{";
	for (map<string, Building>::iterator i = currBuilds.begin(); i != currBuilds.end(); i++) {
		if (i != currBuilds.begin()) {
			cout << ", ";
		}
		cout << i->first << " : " << i->second.str();
	}
	cout << "}\n";
}

struct cmp {
	bool operator()(const pair<int, string>& p1, const pair<int, string>& p2) {
		return p1.first > p2.first;
	}
};
void Cluster::recursion(map<string, Building>& currBuilds, const vector<string>& plist, unsigned int& count, unsigned int iter = 0) {
	if (plist.empty()) {
		// cout << "empty" << endl;
		return;
	}

	if (iter == plist.size()) {
		int currCPS = calcCPS(currBuilds);
		if (currCPS > maxVal) {
			maxVal = currCPS;
			maxMap = currBuilds;
		}

		count += 1;
		if (count % 100000 == 0) {
			cout << fixed << setprecision(3) << time(0)-startTime << " - " << setprecision(0) << count << endl;
		}
		return;
	}

	// for each job, try to assign it to a workplace
	// if it works, recurse through to next job
	// else, skip
	for (int i = Workplace1; i <= Workplace3; i++) {
		string build = jobs->at(plist[iter]).at(Workplace1 + i);
		if (!build.empty()) {
			currBuilds[build].insertJob(plist[iter]);
		}

		recursion(currBuilds, plist, count, iter+1);

		currBuilds[build].removeJob(plist[iter]);
	}
}
int Cluster::getMax() {
	if (done) {
		return maxVal;
	}

	// set up data
	map<string, Building> builds;
	vector<string> *row;

	for (auto b : this->qbmap) {
		row = &buildings->at(b.first);
		Building temp(row);
		builds[b.first] = temp;
	}

	map<string, int> qpmap = this->qpmap;
	filterFit(builds, qpmap);		// useful to make obvious choices

	vector<string> people;
	for (map<string, int>::iterator i = qpmap.begin(); i != qpmap.end(); i++) {
		while (i->second > 0) {
			people.push_back(i->first);
			qpmap[i->first]--;
		}
	}

	filterEasy(builds, people);		// useful to make obvious choices
	maxVal = calcCPS(builds);
	maxMap = builds;
	cout << "Trimmed. " << people.size() << " people remain." << endl;

	cout << "About 3^" << people.size() << " permutations." << endl;

	startTime = time(0);
	unsigned count = 0;			// used for update log
	recursion(builds, people, count);
	cout << "Finished calculation.\n";
	cout << "Total time: " << time(0)-startTime << "\n";
	cout << endl;

	done = true;

	return maxVal;
}

string Cluster::configStr() {
	if (!done) {
		getMax();
	}

	string ans;
	// can't use printMap(), so gotta write it normally
	ans = "";
	for (map<string, Building>::iterator i = maxMap.begin(); i != maxMap.end(); i++) {
		if (i != maxMap.begin())
			ans.append("\n");
		ans.append(i->second.str());
	}

	return ans;
}


// create a vector of sets that have all connected buildings and people
vector<set<string>> generateClusters(const map<string, vector<string>>& buildings) {
	vector<set<string>> ans;

	// for each building
	// get the jobs that can go there and throw them all in a set
	// if we encounter a job that we have already seen, union the sets
	// finally, push to ans
	set<string> temp;
	for (auto& i: buildings) {						// for each line of buildings
		temp.clear();

		temp.insert(i.second.at(Building_name));
		for (unsigned j = Worker1; j <= Worker6; j++) {
			if (!i.second[j].empty()) {
				temp.insert(i.second[j]);
			}
		}
		// cout << setToStr(temp) << endl;

		for (unsigned k = 0; k < ans.size(); k++) {		// for every set saved
			for (auto& j: temp) {						// iterate through temp, looking for values
				if (ans.at(k).find(j) != ans.at(k).end()) {
					temp.merge(ans.at(k));
					ans.at(k).clear();
					break;
				}
			}
		}
		ans.push_back(temp);
	}

	// clean up ans by removing all empty sets used
	vector<set<string>> ret;
	for (unsigned i = 0; i < ans.size(); i++) {
		if (!ans.at(i).empty())
			ret.push_back(ans.at(i));
	}

	// sort vector by set size
	auto cmp = [](const set<string>& s1, const set<string>& s2) { return s1.size() < s2.size(); };
	sort(ret.begin(), ret.end(), cmp);

	cout << ret.size() << " clusters generated.\n";
	
	return ret;
}
