#ifndef __CSVREADER__
#define __CSVREADER__

#include <vector>
#include <string>
#include <map>

// I just made this work similarly to pandas
class CSVReader {
  private:
	std::string test;
	std::vector<std::string> strip(const std::string&, char) const;			// implementation of Python's .strip()
	std::vector<std::vector<std::string>> readCSV(const std::string&) const;

  public:
	CSVReader(const std::string&);
	std::map<std::string, std::vector<std::string>> getDataframeFromCSV(const std::string&) const;
	std::map<std::string,int> getMapFromCSV(const std::string&) const;
};

#endif