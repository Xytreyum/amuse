# standard amuse configuration include
# config.mk will be made after ./configure has run
AMUSE_DIR?=../../../..
-include ${AMUSE_DIR}/config.mk

MPIFC ?= mpif90
FORTRAN ?= gfortran
FC ?= $(FORTRAN)


CODE_GENERATOR = $(AMUSE_DIR)/build.py

SRCDIR=src/code
BUILDDIR=build

CMAKE_DEPS=src/CMakeLists.txt src/cmake/CompilerFlags.cmake src/cmake/FileList.cmake

SRC = $(SRCDIR)/library_v2.f90 $(SRCDIR)/export.f90 $(SRCDIR)/import.f90 \
      $(SRCDIR)/create_new_model.f90 $(SRCDIR)/prtoft.f90

EVTWINLIB=$(BUILDDIR)/libtwin.a

FLIB= -L/software/local/intel64/compiler91/lib -lifcore -lifport
LD = ld
AR = ar ruv
RANLIB = ranlib
CMAKE_GENERATOR ?= Unix Makefiles

all:    $(BUILDDIR)/Makefile evtwin_worker

$(BUILDDIR)/Makefile: $(CMAKE_DEPS)
	-mkdir -p $(BUILDDIR)
	cd $(BUILDDIR) && FC="$(FC) $(FCFLAGS)" cmake ../src -DCMAKE_Fortran_FLAGS:STRING="$(FCFLAGS)"  -G "$(CMAKE_GENERATOR)"

clean:
	rm -f *.pyc make.log
	rm -f mpi_code.f90 worker_code evtwin_worker twin_library_v2.mod mesh.mod evtwin_worker_sockets worker_code-sockets.f90 forsockets.mod
	rm -f amuse_worker_module.mod
	rm -f worker_code.f90
	rm -f $(BUILDDIR)/CMakeCache.txt
	rm -rf $(BUILDDIR)/CMakeFiles
	rm -rf $(BUILDDIR)/Makefile
	rm -rf $(BUILDDIR)

distclean:
	make -C src distclean
	/bin/rm -f *.pyc

evtwin_worker: worker_code.f90 $(SRC)
	make -s --no-print-directory -C $(BUILDDIR)
	$(MPIFC) -I$(BUILDDIR) $(FS_FLAGS) $< -o $@ $(EVTWINLIB) $(FS_LIBS)  $(LIBS)

worker_code.f90: interface.py
	$(CODE_GENERATOR) --type=f90 interface.py EVtwinInterface -o $@
