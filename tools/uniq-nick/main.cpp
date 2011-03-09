#include <iostream>
#include <unordered_set>
#include <string>
#include <openssl/md5.h>
#include <string.h>

using namespace std;

uint32_t get_tok(string s) {
	MD5_CTX md5c;
	unsigned char final[16];
	uint32_t rlt;

	MD5_Init(&md5c);
	MD5_Update(&md5c, s.c_str(), s.length());
	MD5_Final(final, &md5c);
	memcpy((void*) &rlt, (void*) final, 4);

	return rlt;
}

int main(int argc, const char *argv[]) {
	string buf;
	unordered_set<uint32_t> set;

	while (cin >> buf) {
		uint32_t tok = get_tok(buf);
		if (set.find(tok) == set.end()) {
			cout << buf << endl;
			set.insert(tok);
		}
	}

	return 0;
}
