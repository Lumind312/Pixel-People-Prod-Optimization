#include "Cluster.h"
#include <bits/stdc++.h>
#include "DF_Headers.h"
#include "Prints.h"
using namespace std;

// default constructor
// needed for default creation in builds map, but there are branches in functions (that return 0) just in case
Building::Building() {
	info = nullptr;
	maxCPS = 0;
	multiplier = 0;
	// workers.clear()
	// fullCPS = false;
}

// input is address of the dataframe row and quantity
Building::Building(vector<string>* building, int num = 1) : info(building) {
	maxCPS = stoi(info->at(MaxCPS));
	multiplier = stoi(info->at(Multiplier).substr(1));
	workers.resize(num);	// will create num number of empty sets
	currCPS.resize(num, 0);
}

// print workers
string Building::str() const {
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
unsigned int Building::len() const {
	return workers.size();
}
// clear all sets in workers
void Building::clear() {
	for (unsigned i = 0; i < workers.size(); i++)
		workers.at(i).clear();
}


// true if job can and was added, false if not
bool Building::insertJob(const string& j) {
	if (info == nullptr)
		return false;

	unsigned int prev_size;
	for (unsigned i = 0; i < workers.size(); i++) {
		prev_size = workers.at(i).size();
		workers.at(i).insert(j);
		if (prev_size != workers.at(i).size()) {
			currCPS.at(i) += multiplier;
			return true;
		}
	}
	return false;
}
// true if job exists and was removed, false if not
// go from the back of the list to make cps front-heavy
bool Building::removeJob(const string& j) {
	if (info == nullptr)
		return false;

	unsigned int prev_size;
	for (int i = int(workers.size())-1; i >= 0; i--) {
		prev_size = workers.at(i).size();
		workers.at(i).erase(j);
		if (prev_size != workers.at(i).size()) {
			currCPS.at(i) -= multiplier;
			return true;
		}
	}
	return false;
}

// calculate all building CPS based on number of workers
int Building::getCPS() const {
	if (info == nullptr)
		return 0;
	int sum = 0;
	for (unsigned i = 0; i < currCPS.size(); i++)
		sum += currCPS.at(i);
	return sum;
}
// a hypothetical "what if we remove this person"
int Building::oneLess() const {
	int c = getCPS();
	if (c == 0)
		return -1;

	if (c == maxCPS)
		c /= 2;
	return c - multiplier;
}
// a hypothetical "what if we add this person"
int Building::oneMore() const {
	int c = getCPS();
	if (c == maxCPS)
		return -1;
	if (c == 0)
		return 0;
	return c - multiplier;
}

Job::Job(int num = 0) {
	this->people.resize(num);
	sz = num;
	curr = 0;
}
string Job::getLowest() {
	return this->people.at(curr);
}
void Job::AssignWorkplace(const string& w) {
	this->people.at(curr++) = w;
	if (curr > sz)
		curr = 0;
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
		currPerson = people.at(i).substr(0, people.at(i).size()-1);
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
void Cluster::createConfig(map<string, Building>& currBuilds, map<string, Job>& plist) {
	cout << "Creating config\n";
	if (plist.empty()) {
		// cout << "empty" << endl;
		return;
	}

	// get rid of any empty building slots
	if (currBuilds.find("") != currBuilds.end()) {
		currBuilds.erase("");
	}
	if (plist.find("") != plist.end()) {
		plist.erase("");
	}

	priority_queue<pair<int, string>, vector<pair<int, string>>, cmp> pq;		// (multiplier, building name)
	pair<int, string> temp;

	cout << "currBuilds:" << endl;

	// populate the pqueue in ascending order by maxCPS
	cout << currBuilds.begin()->first << endl;
	for (map<string, Building>::iterator b = currBuilds.begin(); b != currBuilds.end(); b++) {
		temp = make_pair(b->second.maxCPS, b->first);
		// cout << "a " << b->first << " " << b->second.str() << endl;
		pq.push(temp);
	}
	
	// just prints
	// cout << "Priority queue:" << endl;
	// while (!pq.empty()) {
	// 	cout << pq.top().first << " " << pq.top().second << endl;
	// 	pq.pop();
	// }
	// cout << "end" << endl;

	// have a queue of buildings, from least CPS to most CPS
	// for each building, do a basic fill (for people who have not been assigned jobs yet)
	// then, try to max production by removing people from other buildings and putting them in this building
	// if greater, then keep it. else, reset

	// string curr;
	// Building b;
	// while (!pq.empty()) {
	// 	curr = pq.top().second;
	// 	pq.pop();

	// 	b = currBuilds[curr];
	// 	for (unsigned i = 0) {
			
	// 	}
	// }
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
		Building temp(row, b.second);
		builds[b.first] = temp;
	}

	map<string, int> qpmap = this->qpmap;
	// filterFit(builds, qpmap);		// useful to make obvious choices

	// vector<string> people;
	// for (map<string, int>::iterator i = qpmap.begin(); i != qpmap.end(); i++) {
	// 	while (i->second > 0) {
	// 		people.push_back(i->first + to_string(i->second));
	// 		qpmap[i->first]--;
	// 	}
	// }
	map<string, Job> people;
	for (map<string, int>::iterator i = qpmap.begin(); i != qpmap.end(); i++) {
		people[i->first] = Job(i->second);
	}

	// filterEasy(builds, people);		// useful to make obvious choices
	builds.erase("");
	maxVal = calcCPS(builds);
	maxMap = builds;
	cout << "Trimmed. " << people.size() << " people remain." << endl;

	// auto start = time(0);
	createConfig(builds, people);
	cout << "Finished calculation.\n";
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
