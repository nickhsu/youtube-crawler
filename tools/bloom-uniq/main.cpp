#include <stdlib.h>
#include <time.h>
#include <stdio.h>
#include <unistd.h>

#include "bloom_filter.hpp"

const int BUF_SIZ = 4096;

void usage() {
		printf("usage: bloom-uniq -e error_rate -n num_item < file_name\n");
}

int main(int argc, char *argv[]) {
	int num_item, ch;
	float error_rate;

	while ((ch = getopt(argc, argv, "e:n:")) != -1) {
		switch (ch) {
		case 'e':
			error_rate = atof(optarg);
			break;
		case 'n':
			num_item = atoi(optarg);
			break;
		case '?':
		default:
			usage();
			exit(1);
			break;
		}
	}

	srand (time(NULL));
	bloom_filter filter(num_item, error_rate, rand());

	char buffer[BUF_SIZ];
	while (fgets(buffer, BUF_SIZ, stdin)) {
		int len = strlen(buffer);
		if (filter.contains(buffer, len) == false) {
			puts(buffer);
			filter.insert(buffer, len);
		}
	}

	return 0;
}
