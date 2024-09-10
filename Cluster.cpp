#include "Cluster.h"
#include <bits/stdc++.h>
#include "DF_Headers.h"
#include "Prints.h"
using namespace std;

// default constructor
// needed for default creation in builds map, but there are branches in functions (that return 0) just in case
Cluster::Building::Building() {
	info = nullptr;
	// workers.clear()
	// fullCPS = false;
}

// input is address of the dataframe row and quantity
Cluster::Building::Building(vector<string>* building, int num = 1) : info(building) {
	workers.resize(num);	// will create num number of empty sets
}

// print workers
string Cluster::Building::str() const {
	string ans = "[";
	for (unsigned int i = 0; i < workers.size(); i++) {
		if (i > 0) {
			ans.append(", ");
		}
		ans.append(setToStr(workers.at(0)));
	} ans.append("]");
	return ans;
}
// return number of this type of building (workers.size())
unsigned int Cluster::Building::len() const {
	return workers.size();
}
// clear all sets in workers
void Cluster::Building::clear() {
	for (unsigned i = 0; i < workers.size(); i++) {
		workers.at(i).clear();
	}
}


// true if job can and was added, false if not
bool Cluster::Building::insertJob(const string& j) {
	if (info == nullptr)
		return false;

	unsigned int prev_size;
	for (unsigned i = 0; i < workers.size(); i++) {
		prev_size = workers.at(i).size();
		workers.at(i).insert(j);
		if (prev_size != workers.at(i).size())
			return true;
	}
	return false;
}
// true if job exists and was removed, false if not
bool Cluster::Building::removeJob(const string& j) {
	if (info == nullptr)
		return false;

	unsigned int prev_size;
	for (unsigned i = 0; i < workers.size(); i++) {
		prev_size = workers.at(i).size();
		workers.at(i).erase(j);
		if (prev_size != workers.at(i).size())
			return true;
	}
	return false;
}

// int Cluster::Building::totalMult() const {
// 	if (!fullCPS) {
// 		return 1;
// 	}
// }
// calculate all building CPS based on number of workers
int Cluster::Building::getCPS() const {
	if (info == nullptr)
		return 0;

	int sum = 0, multiplier;
	for (auto& i: workers) {
		// if we have a full number of people, use maxcps
		if (i.size() == unsigned(stoi(info->at(Capacity)))) {
			sum += stoi(info->at(MaxCPS));
		}
		else {
			multiplier = stoi(info->at(Multiplier).substr(1));
			sum += multiplier * i.size();
		}
	}
	return sum;
}

// -------------------

Cluster::Cluster(map<string, vector<string>> *buildings, map<string, vector<string>> *jobs, const map<string, int>& qbmap, const map<string, int>& qpmap) :
buildings(buildings), jobs(jobs), qbmap(qbmap), qpmap(qpmap) {
	maxVal = 0;
	count = 0;
	total = 0;
	exponent = 0;

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
		currPerson = people.at(i).substr(0, people.at(i).size()-1);
		currRow = jobs->at(currPerson);
		
		// needs to have only 1 workplace.
		// should have a spot guaranteed
		if (!(stoi(currRow.at(Options)) == 1 && builds[currRow.at(Workplace1)].insertJob(currPerson))) {
			newp.push_back(people.at(i));
		}
	}
	people = newp;
}
// assign jobs where we have a one-to-one quantity between the job and their buildings
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
			curr.at(j) += builds[currRow.at(j+Workplace1)].len();
			sum += curr.at(j);
		}

		// if the numbers match, put them in buildings and remove the job
		if (sum == i.second) {
			for (unsigned j = 0; j < 3 && !currRow.at(j).empty(); j++) {
				while (curr.at(j)) {
					builds[currRow.at(j+Workplace1)].insertJob(i.first);
					curr.at(j)--;
				}
			}
			qpmap.erase(i.first);
		}
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
void printState(map<string, Cluster::Building>& currBuilds) {
	cout << "State:\n{";
	for (map<string,Cluster::Building>::iterator i = currBuilds.begin(); i != currBuilds.end(); i++) {
		if (i != currBuilds.begin()) {
			cout << ", ";
		}
		cout << i->first << " : " << i->second.str();
	}
	cout << "}\n";
}

// iterate through keys and get a value to save
// also uses this->count to keep track of progress (how much the algorithm has done)
void Cluster::recursion(map<string, Building>& currBuilds, const vector<string>& plist, unsigned iter = 0) {
	// base case: we have reached the end of the people
	if (iter == plist.size()) {
		// progress record
		this->count++;
		if (this->count % 100000 == 0 || (this->count == this->total && this->ce >= this->exponent)) {
			if (count > 1000000000) {
				this->ce += 9;
				count = 0;
			}
			cout << "Generated " << this->count << "e" << this->ce << " of " << this->total << "e" << exponent << " permutations.\n";
		}
		
		// see if current config has highest value
		int val = calcCPS(currBuilds);
		if (val > this->maxVal) {
			this->maxVal = val;
			this->maxMap = currBuilds;		// should be an easy transfer? but not efficient in terms of space probably
		}
		return;
	}

	vector<string> workplaces = {};		// can add "" if there can be person with no job
	string currJob = plist[iter].substr(0, plist[iter].size()-1);	// remove the id number when adding to building
	vector<string> currRow = jobs->at(currJob);
	for (unsigned i = Workplace1; i <= Workplace3 && !currRow.at(i).empty(); i++) {
		if (currBuilds.find(currRow[i]) != currBuilds.end())
		workplaces.push_back(currRow.at(i));
	}

	for (auto w: workplaces) {
		// make sure we can actually have the building and can add it
		if (currBuilds[w].insertJob(currJob)) {
			recursion(currBuilds, plist, iter+1);

			currBuilds[w].removeJob(currJob);
		}
	}

}
int Cluster::getMax() {
	if (done) {
		return maxVal;
	}

	// set up data
	map<string, Building> builds;
	vector<string> *row;
	for (auto b: this->qbmap) {
		row = &buildings->at(b.first);
		Building temp(row, b.second);
		builds[b.first] = temp;
	}

	map<string, int> qpmap = this->qpmap;
	filterFit(builds, qpmap);		// useful to make obvious choices

	vector<string> people;
	for (map<string, int>::iterator i = qpmap.begin(); i != qpmap.end(); i++) {
		while (i->second > 0) {
			people.push_back(i->first + to_string(i->second));
			qpmap[i->first]--;
		}
	}

	filterEasy(builds, people);		// useful to make obvious choices
	cout << "Trimmed. " << people.size() << " people remain." << endl;

	// calculate how long it will take
	total = 1;
	long num;
	for (auto i: people) {
		if (jobs->find(i.substr(0, i.size()-1)) == jobs->end()) {
			cout << "Error: " << i.substr(0, i.size()-1) << " does not exist in jobs.csv." << endl;
			exit(1);
		}
		num = stoul(jobs->at(i.substr(0, i.size()-1)).at(Options));
		total *= num;
		if (total > 1000000000) {
			exponent += 9;
			total /= 1000000000;
		}
		cout << "Total: " << total << "e" << exponent << endl;
	}
	cout << "Need to generate " << total << "e" << exponent << " cases.\n";

	// auto start = time(0);
	recursion(builds, people);
	cout << "Finished recursion.\n";
	// cout << "Total time: " << time(0)-start << "\n";
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
	ans = "{";
	for (map<string, Building>::iterator i = maxMap.begin(); i != maxMap.end(); i++) {
		if (i != maxMap.begin())
			ans.append(", ");
		ans.append(i->first);
		ans.append(" : ");
		ans.append(i->second.str());
	}
	ans.append("}\n");

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
	for (auto& i: buildings) {
		temp.clear();

		temp.insert(i.second[Building_name]);
		for (unsigned j = Worker1; j <= Worker6; j++) {
			if (!i.second[j].empty()) {
				temp.insert(i.second[j]);
			}
		}
		// cout << setToStr(temp) << endl;

		for (unsigned k = 0; k < ans.size(); k++) {
			for (auto& j: temp) {
				if (ans.at(k).find(j) != ans.at(k).end()) {
					temp.merge(ans.at(k));
					ans.at(k).clear();
					continue;
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
