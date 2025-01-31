#ifndef __CLUSTER__
#define __CLUSTER__

// originally created in python
// #include <bits/stdc++.h>

#include <vector>
#include <string>
#include <map>
#include <set>

// class for holding buildings
class Building {
  public:
	Building();
	Building(std::vector<std::string>* info, int num);
	
	std::string str() const;
	unsigned int len() const;
	void clear();

	bool insertJob(const std::string&);
	bool removeJob(const std::string&);
	// int totalMult() const;
	int getCPS() const;
	int oneLess() const;		// may be unnecessary
	int oneMore() const;		// may be unnecessary

	int maxCPS, multiplier;
  private:
	std::vector<std::string> *info;					// row of building data
	std::vector<std::set<std::string>> workers;		// one set per building
	std::vector<int> currCPS;
	
	// std::vector<int> workingTimes;	// times of buildings (in minutes)
	// bool fullCPS;
};
// holds where people work
class Job {
  public:
	Job(int);
	std::string getLowest();	// returns the name of the building to be replaced next
	void AssignWorkplace(const std::string&);
  private:
	std::vector<std::string> people;	// list of people's workplaces
	int sz;
	int curr;			// next person to replace
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

	void filterEasy(std::map<std::string, Building>& builds, std::vector<std::string>& people);
	void filterFit(std::map<std::string, Building>& builds, std::map<std::string, int>& qpmap);
	int calcCPS(const std::map<std::string, Building>& bdict) const;
	void createConfig(std::map<std::string, Building>& currBuilds, std::map<std::string, Job>& plist);

  public:
	Cluster(std::map<std::string, std::vector<std::string>> *buildings, std::map<std::string, std::vector<std::string>> *jobs, const std::map<std::string, int>& qbmap, const std::map<std::string, int>& qpmap);
	std::string str();
	
	int getMax();
	std::string configStr();
};

std::vector<std::set<std::string>> generateClusters(const std::map<std::string,std::vector<std::string>>&);

#endif