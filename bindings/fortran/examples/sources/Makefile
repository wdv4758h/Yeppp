ifeq ($(FC),gfortran)
FFLAGS += -O3
FFLAGS += -march=native
FFLAGS += -std=f2003
endif

ifeq ($(FC),ifort)
FFLAGS += -O3
FFLAGS += -xHost
FFLAGS += -std03
endif

all: Entropy

Entropy: Entropy.f90
	$(FC) -I../../sources -L../../../../library/binaries/x64-linux-sysv-default Entropy.f90 -o Entropy -lyeppp

run: all
	LD_LIBRARY_PATH=${PWD}/../../../../library/binaries/x64-linux-sysv-default ./Entropy
