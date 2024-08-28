// priority queue of buildings, in descending order of the most money (make it a function so I can change it out if needed)
// two building options: one with the double (x2) cps, and one with the single (x1) cps
// that way, we try the double first, then try the single if the double fails.
// for now, assume that we only have one of each building. I'll think of if we have 2 later down the line maybe

#include <bits/stdc++.h>
using namespace std;
#include <queue>

const int MAX_WORKERS = 6;
// const int MAX_JOBS = 3;
string test;								// use test files by putting an argument in command line
vector<string> strip(const string&);	// implementation of Python's .strip()

class Building {
  public:
	string name;
	vector<string> workers;
	
	void csvToBuilding(const string& s);
	bool operator<(const Building&) const;
	string str() const;
	void clear();
	Building halfCPS() const;

  private:
	bool full = false;		// tells the > comparator which system to use (maxcps or prod)
	int multiplier;			// how much each worker contributes
	int maxcps;				// either using the x2 boost, or just the normal one
	int prod;				// cps * time
	
};

void readCSV(const string& filename, vector<Building>& vb) {
	// get quantities first

	ifstream qFS;
	string f = "qbuilding.csv";
	if (!test.empty()) {
		f = "tests/" + test + "/" + f;
	}
	qFS.open(f);
	if (!qFS.is_open()) {
		cout << "Error: \"" << f << "\" does not exist." << endl;
		exit(1);
	}
	string temp;
	map<string, int> qmap;
	getline(qFS, temp);
	while (getline(qFS, temp)) {
		qmap[temp.substr(0, temp.find(','))] = stoi(temp.substr(temp.find(',')+1));
	}
	
	ifstream inFS(filename);
	if (!inFS.is_open()) {
		cout << "Error: " << filename << " does not exist." << endl;
		exit(1);
	}

	getline(inFS, temp);	// save the header?

	Building b;
	while (getline(inFS, temp)) {
		b.csvToBuilding(temp);
		if (qmap.find(b.name) != qmap.end()) {
			for (int i = 0; i < qmap[b.name]; i++) {
				vb.push_back(b);
				vb.push_back(b.halfCPS());
			}
		}
		b.clear();
	}
}
void PrintPriorityQueue(const priority_queue<Building>& pq) {
	priority_queue<Building> temp = pq;
	cout << "PQ Size: " << pq.size() << "\n";
	while (!temp.empty()) {
		cout << temp.top().str() << "\n";
		temp.pop();
	}
}

void permutation(vector<Building> vb) {
	
}

int main(int argc, char* argv[]) {
	test = argc > 1;

	vector<Building> vb;
	string f = "buildings.csv";
	if (argc > 1) {
		test = argv[1];
		f = "tests/" + test + "/" + f;
	}
	readCSV(f, vb);

	priority_queue<Building> pq;

	for (vector<Building>::iterator i = vb.begin(); i != vb.end(); i++) {
		pq.push(*i);
	}

	PrintPriorityQueue(pq);

	return 0;
}

vector<string> strip(const string& s) {
	string temp = s;
	if (temp.find('\n') != string::npos) {
		cout << "Found \'\n\'. Trimming string...";
		temp = temp.substr(0, temp.find('\n'));
	}
	
	vector<string> ret;
	while (temp.find(',') != string::npos) {
		ret.push_back(temp.substr(0, temp.find(',')));
		temp = temp.substr(temp.find(',')+1);
	}
	ret.push_back(temp);
	return ret;
}
void Building::csvToBuilding(const string& s) {
	vector<string> v = strip(s);

	this->name = v[0];							// ["Building name"]
	this->maxcps = stoi(v[2]);					// ["MaxCPS"]
	this->multiplier = stoi(v[3].substr(1));	// ["Multiplier"]
	for (unsigned i = 0; i < 6; i++)
		this->workers.push_back(v[i+4]);		// ["Worker1", "Worker2", ...]
}

string Building::str() const {
	string ret = this->name;
	ret.append(" " + to_string(this->maxcps));
	ret.append(" x" + to_string(this->multiplier));
	for (int i = 0; i < MAX_WORKERS; i++) {
		ret.append(" " + this->workers.at(i));
	}

	return ret;
}
void Building::clear() {
	this->name.clear();
	this->maxcps = 0;
	this->multiplier = 0;
	this->prod = 0;
	this->workers.clear();
}

Building Building::halfCPS() const {
	Building b = *this;
	b.name.append("-half");
	b.maxcps /= 2;
	return b;
}

bool Building::operator<(const Building& rhs) const {
	if (!full)
		return this->maxcps < rhs.maxcps;
	else
		return this->prod < rhs.prod;
}