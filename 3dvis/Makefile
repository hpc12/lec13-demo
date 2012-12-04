# Install libsilo either by downloading and installing from
#
#   https://wci.llnl.gov/codes/silo/
#
# or from Debian/Ubuntu as
#
#   libsilo-dev

EXECUTABLES = write-silo

all: $(EXECUTABLES)

write-silo: write-silo.c
	gcc -std=gnu99 $(DEBUG_FLAGS) -lsiloh5 -o$@ $^

clean:
	rm -f $(EXECUTABLES) *.o
