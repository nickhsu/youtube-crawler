#include <stdio.h>
#include <sys/types.h>
#include <sys/uio.h>
#include <unistd.h>
#include <fcntl.h>

int main(int argc, const char *argv[])
{
		size_t buf_size = 1024 * 4,
			   size_read;
		int fd = open(argv[1], O_RDONLY),
			i,
			num_line = 0;
		char buf[buf_size];

		while ((size_read = read(fd, buf, buf_size)) != 0) {
				for (i = 0; i < size_read; i++) {
						if (buf[i] == '\n') {
								num_line++;
						}
				}
		}

		printf("%d\n", num_line);
		return 0;
}
