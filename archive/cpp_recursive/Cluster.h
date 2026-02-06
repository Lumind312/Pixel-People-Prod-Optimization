#ifndef __CLUSTER__
#define __CLUSTER__

// originally created in python
// #include <bits/stdc++.h>

#include <vector>
#include <string>
#include <map>
#include <set>

// class for holding buildings
// one building per type
class Building {
  public:
	Building();
	Building(std::vector<std::string>* info, int num);
	
	std::string str() const;
	void clear();

	bool insertJob(const std::string&);
	bool removeJob(const std::string&);
	// int totalMult() const;
	int getCPS() const;

	std::string name;
	int maxCPS, multiplier, quantity;
  private:
	std::vector<std::string> *info;					// row of building data
	std::map<std::string, int> workers;				// count how many of each worker
	
	// std::vector<int> workingTimes;	// times of buildings (in minutes)
	// bool fullCPS;
};

class Cluster {
  private:
	friend void printState(std::map<std::string, Building>&);		// debugging function

	// reference to the data
	std::map<std::string, std::vector<std::string>> *buildings, *jobs;
	// quantities of buildings and people
	std::map<std::string, int> qbmap, qpmap;

	int maxVal;
	std::map<std::string, Building> maxMap;
	bool done;		// so it doesn't have to calculate more than once
	int startTime;
	bool displayed = true;

	void filterEasy(std::map<std::string, Building>& builds, std::vector<std::string>& people);
	void filterFit(std::map<std::string, Building>& builds, std::map<std::string, int>& qpmap);
	int calcCPS(const std::map<std::string, Building>& bdict) const;
	void recursion(std::map<std::string, Building>& currBuilds, const std::vector<std::string>& plist, unsigned int& count, unsigned int iter);		// count is used for update log

  public:
	Cluster(std::map<std::string, std::vector<std::string>> *buildings, std::map<std::string, std::vector<std::string>> *jobs, const std::map<std::string, int>& qbmap, const std::map<std::string, int>& qpmap);
	std::string str();
	
	int getMax();
	std::string configStr();
};

std::vector<std::set<std::string>> generateClusters(const std::map<std::string,std::vector<std::string>>&);

#endif