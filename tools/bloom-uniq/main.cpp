#include <iostream>
#include <string>
#include <stdlib.h>
#include <time.h>
#include <stdio.h>

#include "bloom_filter.hpp"


using namespace std;

const int FILTER_SIZE = 100000;
const float ERROR_RATE = 0.01;
const int BUF_SIZ = 4096;

int main(int argc, const char *argv[]) {
	srand (time(NULL));
	bloom_filter filter(FILTER_SIZE, ERROR_RATE, rand());


	char buffer[BUF_SIZ];
	while (fgets(buffer, BUF_SIZ, stdin)) {
		int len = strlen(buffer);
		if (filter.contains(buffer, len) == false) {
			cout << buffer << endl;
			filter.insert(buffer, len);
		}
	}

	/*
	string buffer;
	while (getline(cin, buffer)) {
		if (filter.contains(buffer) == false) {
			cout << buffer << endl;
			filter.insert(buffer);
		}
	}
	*/


	return 0;
}
