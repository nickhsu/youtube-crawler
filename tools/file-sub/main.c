#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define BUF_SIZ 1024000 // 100k

void usage() {
        printf("usage: file-sub file1 file2\n");
}

int main(int argc, const char *argv[]) {
        char buf_a[BUF_SIZ], buf_b[BUF_SIZ];
        FILE *fp_a, *fp_b;
        int cmp;

        if (argc != 3) {
                usage();
                exit(0);
        }

        fp_a = fopen(argv[1], "r");
        fp_b = fopen(argv[2], "r");
        if (fp_a == NULL && fp_b == NULL) {
                printf("file open error\n");
                exit(0);
        }

        if (fgets(buf_a, BUF_SIZ, fp_a) == NULL) {
                exit(0);
        }
        if (fgets(buf_b, BUF_SIZ, fp_b) == NULL) {
                printf("%s", buf_a);
                while (fgets(buf_a, BUF_SIZ, fp_a) != NULL) {
                        printf("%s", buf_a);
                }
                exit(0);
        }

        while (1) {
                cmp = strncmp(buf_a, buf_b, BUF_SIZ);
                if (cmp == 0) {
                        fgets(buf_a, BUF_SIZ, fp_a);
                } else if (cmp < 0) {
                        printf("%s", buf_a);
                        fgets(buf_a, BUF_SIZ, fp_a);
                } else {
                        fgets(buf_b, BUF_SIZ, fp_b);
                }

                if (feof(fp_a)) {
                        break;
                }
                if (feof(fp_b)) {
                        while (fgets(buf_a, BUF_SIZ, fp_a) != NULL) {
                                printf("%s", buf_a);
                        }
                }
        }

        return 0;
}