#include "Prints.h"
#include <bits/stdc++.h>
using namespace std;

void printDF(const vector<vector<string>>& df) {
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
void printMap(const map<string,int>& m) {
	cout << "{";
	for (auto i = m.begin(); i != m.end(); i++) {
		if (i != m.begin())
			cout << ", ";
		cout << i->first << ":" << i->second;
	}
	cout << "}" << endl;
}

string setToStr(const set<string>& s) {
	string ans = "{";
	for (set<string>::const_iterator i = s.cbegin(); i != s.cend(); i++) {
		if (i != s.cbegin())
			ans.append(", ");
		ans.append(*i);
	} ans.append("}");
	return ans;
}

