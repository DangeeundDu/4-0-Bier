# warnlevel and flags
WARNLEVEL   = -Wall -Werror -Wextra
CFLAGS      = -c $(WARNLEVEL) -D _XOPEN_SOURCE=500 -D _DEFAULT_SOURCE -std=c99 -pedantic -I... #_XOPEN_SOURCE >= 500 needed for snprintf()

# compiler name
CC          = gcc

# shell name
SHELL       = /bin/sh

PROG = pizzaservice
HRC = pizzaservice.progh
SRC = chkdata.prog create.prog order.prog view.prog pizzaservice.prog 
OBJ = $(SRC:%.prog=.%.o)
TMP = $(SRC:%.prog=.%.c)
CL = $(TMP) $(TMP:%.c=%.h) $(OBJ)

.PHONY:
all: $(PROG)

$(PROG): $(OBJ) 
	@$(CC) $^ -o $@
	@echo $(PROG)
	@rm -f $(CL)

dep: $(SRC:%.prog=.%.c) $(HRC:%.progh=.%.h)
	@$(CC) -MM $(SRC:%.prog=.%.c) > .depend
	
-include .depend

.%.o: 
	@$(CC) $(CFLAGS) $<
	@-rm $<
	@echo .

.%.c: %.prog 
	@sed 's,\<GET\>,#include,g' $< | sed 's,\([^ "<]*\)\.progh\>,\.\1\.h,g' | sed 's,INIT_MYLANG,#include<.mylang.h>,g' | sed 's,GUARD(\([^)]*\)),#ifndef \1\n#define \1,g' | sed 's,ENDGUARD,#endif,g' | sed 's,DECLARE,#define,g' | sed 's,\<EQUAL\>,=,g' > $@
	
.%.h: %.progh
	@sed 's,\<GET\>,#include,g' $< | sed 's,\([^ "<]*\)\.progh\>,\.\1\.h,g' | sed 's,INIT_MYLANG,#include<.mylang.h>,g' | sed 's,GUARD(\([^)]*\)),#ifndef \1\n#define \1,g' | sed 's,ENDGUARD,#endif,g' | sed 's,DECLARE,#define,g' | sed 's,\<EQUAL\>,=,g' > $@

clean-bu:
	-rm *~

clean:
	@-rm -f $(CL) $(PROG)

distclean: clean clean-bu 

