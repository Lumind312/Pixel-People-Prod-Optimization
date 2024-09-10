#ifndef __CLUSTER__
#define __CLUSTER__

// originally created in python
// #include <bits/stdc++.h>

#include <vector>
#include <string>
#include <map>
#include <set>
class Cluster {
  private:
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
	  private:
		std::vector<std::string> *info;					// row of building data
		std::vector<std::set<std::string>> workers;		// one set per building
		
		// std::vector<int> workingTimes;	// times of buildings (in minutes)
		// bool fullCPS;
	};
	friend void printState(std::map<std::string, Cluster::Building>&);		// debugging function

	// reference to the data
	std::map<std::string, std::vector<std::string>> *buildings, *jobs;
	// quantities of buildings and people
	std::map<std::string, int> qbmap, qpmap;

	int maxVal;
	std::map<std::string, Cluster::Building> maxMap;
	unsigned int count, ce, cthousand;
	unsigned int total, exponent;
	bool done;		// so it doesn't have to calculate more than once

	void filterEasy(std::map<std::string, Building>& builds, std::vector<std::string>& people);
	void filterFit(std::map<std::string, Building>& builds, std::map<std::string, int>& qpmap);
	int calcCPS(const std::map<std::string, Cluster::Building>& bdict) const;
	void recursion(std::map<std::string, Building>& currBuilds, const std::vector<std::string>& plist, unsigned);

  public:
	Cluster(std::map<std::string, std::vector<std::string>> *buildings, std::map<std::string, std::vector<std::string>> *jobs, const std::map<std::string, int>& qbmap, const std::map<std::string, int>& qpmap);
	std::string str();
	
	int getMax();
	std::string configStr();
};

std::vector<std::set<std::string>> generateClusters(const std::map<std::string,std::vector<std::string>>&);

#endif