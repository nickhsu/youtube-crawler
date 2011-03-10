#
# Open Bloom Filter Master MakeFile
# By Arash Partow - 2000
#
# URL: http://www.partow.net/programming/hashfunctions/index.html
#
# Copyright Notice:
# Free use of this library is permitted under the guidelines
# and in accordance with the most current version of the
# Common Public License.
# http://www.opensource.org/licenses/cpl1.0.php
#

COMPILER         = -g++
OPTIMIZATION_OPT = -O3
OPTIONS          = -Wall $(OPTIMIZATION_OPT) -o

BUILD+=bloom-uniq

all: $(BUILD)

bloom-uniq: bloom_filter.hpp main.cpp
	$(COMPILER) $(OPTIONS) bloom-uniq main.cpp


clean:
	rm -f bloom-uniq

#
# The End !
#
