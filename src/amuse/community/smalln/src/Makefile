
# Makefile to build the libsmallN.a library.  The first draft was
# auto-generated; subsequent versions are hand-coded.  Save a copy!

# Optimization may cause failure on some systems.  Replace by -O0 in
# that case.

AMUSE_DIR ?= ../../../../..
OPT	 = -I$(AMUSE_DIR)/lib/stopcond

MPICXX ?= mpicxx
MPICC ?= mpicc
CXX	 ?= mpicxx
CFLAGS   += -g -Wall $(OPT)
CXXFLAGS += $(CFLAGS) 

CODELIB = libsmallN.a

CODEOBJS = smallN-lib.o smallN_unpert.o kepler-lib.o hdyn.o \
	   analyze-lib.o nstab.co f2c.co util.o \
	   smallN_interface.o

AR = ar ruv
RANLIB = ranlib
RM = rm

all: $(CODELIB) 

$(CODELIB): $(CODEOBJS)
	$(RM) -f $@
	$(AR) $@ $(CODEOBJS)
	$(RANLIB) $@

%.o : ../../ph4/src/%.cc
	$(CXX) $(CXXFLAGS) -c -o $@ $^ 

#-----------------------------------------------------------------------
#
# Special cases:

nstab.co:    ../../ph4/src/nstab.c
	$(MPICC) $(CFLAGS) -c $^ -o nstab.co

f2c.co:    ../../ph4/src/f2c.c
	$(MPICC) $(CFLAGS) -c $^ -o f2c.co

smallN-lib.o:	../../ph4/src/smallN.cc
	$(MPICXX) $(CFLAGS) -c $^ -o smallN-lib.o

kepler-lib.o:	../../ph4/src/kepler.cc
	$(MPICXX) $(CFLAGS) -c $^ -o kepler-lib.o

analyze-lib.o:	../../ph4/src/analyze.cc
	$(MPICXX) $(CFLAGS) -c $^ -o analyze-lib.o

#-----------------------------------------------------------------------

tar:
	tar czf smallN.tgz Makefile *.h *.cc plummer*.in*

clean:
	$(RM) -r -f *.o *.co *~ *.tgz *.a
