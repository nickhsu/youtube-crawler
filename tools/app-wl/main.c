#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>

int get_num_line(char *data, int data_size) {
		int count = 0,
			i;

		for (i = 0; i < data_size; i++) {
				if (data[i] == '\n') {
						count++;
				}
		}

		return count;
}

void usage() {
		printf("usage: app-wl -m buffer_size [-n seek_times] file_name\n");
}

int main(int argc, const char *argv[]) {
		char buffer[4096];
		int i, j,
			avg_line_size,
			fd, num_line, buf_size, num_seek = 1, ch;
		long int size_read, total_size_read, file_size;
		char *file_path;

		if (argc == 1) {
				usage();
				exit(1);
		}

		while ((ch = getopt(argc, argv, "m:n:")) != -1) {
				switch (ch) {
				case 'm':
						buf_size = atoi(optarg) * 1024 * 1024; //e.g. 123M
						break;
				case 'n':
						num_seek = atoi(optarg);
						break;
				case '?':
				default:
						usage();
						exit(1);
						break;
				}
		}
		file_path = argv[optind];

		fd = open(file_path, O_RDONLY);
		file_size = lseek(fd, 0L, SEEK_END);

		srand(time(NULL));
		num_line = 0;
		total_size_read = 0;
		for (i = 0; i < num_seek; i++) {
				lseek(fd, rand() % file_size, SEEK_SET);
				for (j = 0; j < buf_size / 4096; j++) {
						size_read = read(fd, buffer, 4096);
						total_size_read += size_read;
						num_line += get_num_line(buffer, size_read);
				}
		}

		avg_line_size = total_size_read / num_line;
		printf("%ld\n", file_size / avg_line_size);

		return 0;
}
