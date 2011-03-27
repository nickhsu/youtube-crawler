#include <iostream>
#include <fstream>
#include <string>
#include <boost/unordered_set.hpp>


using namespace std;

int main(int argc, const char *argv[]) {
		boost::unordered_set<string> set;
		ifstream file1(argv[1]),
				 file2(argv[2]);

		string line;
		while (file2 >> line) {
				set.insert(line);
		}

		while (file1 >> line) {
				if (set.find(line) == set.end()) {
						cout << line << endl;
				}
		}
		return 0;
}
