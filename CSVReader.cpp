#include "CSVReader.h"
#include <bits/stdc++.h>
#include "DF_Headers.h"
using namespace std;

#include <map>

CSVReader::CSVReader(const string& t = "") : test(t) {}

vector<string> CSVReader::strip(const string& s, char token = ',') const {
	string temp = s;
	if (temp.find('\n') != string::npos) {
		cout << "Found \'\n\'. Trimming string...";
		temp = temp.substr(0, temp.find('\n'));
	}
	
	vector<string> ret;
	while (temp.find(token) != string::npos) {
		ret.push_back(temp.substr(0, temp.find(token)));
		temp = temp.substr(temp.find(token)+1);
	}
	ret.push_back(temp);
	return ret;
}

// read CSV and save as a vector of vectors of strings
vector<vector<string>> CSVReader::readCSV(const string& filename) const {
	vector<vector<string>> df;
	string f = test + filename;
	
	ifstream inFS(f);
	if (!inFS.is_open()) {
		cout << "Error: " << f << " does not exist." << endl;
		exit(1);
	}

	string temp;
	getline(inFS, temp);	// save the header? nah
	while (getline(inFS, temp)) {
		df.push_back(this->strip(temp));
	}

	return df;
}
// wrapper that converts a dataframe (vector of vectors of strings) into a map
map<string,int> CSVReader::getMapFromCSV(const string& filename) const {
	map<string,int> m;
	auto df = readCSV(filename);		// inefficient
	for (auto& i: df) {
		m[i.at(Name)] = stoi(i.at(Quantity));
	}

	return m;
}

// add new column with max number of people in buildings or max options of possible buildings per people
// true if for buildings, false if for jobs
vector<vector<string>> CSVReader::getDataframeFromCSV(const string& filename) const {
	auto df = readCSV(filename);
	bool build_job = (filename.at(0) == 'b');

	int count;
	unsigned start = build_job ? Worker1 : Workplace1;
	unsigned end = build_job ? Worker6 : Workplace3;

	for (unsigned i = 0; i < df.size(); i++) {
		count = 0;
		for (unsigned j = start; j <= end; j++)
			count += !df[i][j].empty();
		df.at(i).push_back(to_string(count));
	}

	return df;
}

void printDF(const vector<vector<string>>& df, const string& label) {
	cout << label << ":\n";
	for (unsigned i = 0; i < df.size(); i++) {
		cout << "[";
		for (unsigned j = 0; j < df.at(i).size(); j++) {
			if (j != 0)
				cout << ", ";
			if (df[i][j].empty()) {
				cout << "null";
			}
			else
				cout << df[i][j];
		}
		cout << "]";
		if (i+1 != df.size()) {
			cout << ",";
		}
		cout << "\n";
	}
	cout << endl;
}
void printMap(const map<string,int>& m, const string& label) {
	cout << label << ":\n";
	cout << "{";
	for (map<string,int>::const_iterator i = m.begin(); i != m.end(); i++) {
		if (i != m.begin())
			cout << ", ";
		cout << i->first << ":" << i->second;
	}
	cout << "}\n";
	cout << endl;
}
