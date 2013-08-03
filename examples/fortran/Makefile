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

all: binaries/x64-linux-sysv-default binaries/x64-linux-sysv-default/Entropy

binaries/x64-linux-sysv-default:
	-mkdir -p binaries
	-mkdir -p binaries/x64-linux-sysv-default

binaries/x64-linux-sysv-default/Entropy: binaries/x64-linux-sysv-default sources/Entropy.f90
	$(FC) -I$(YEPROOT)/bindings/fortran/sources -L$(YEPROOT)/binaries/linux/x86_64 sources/Entropy.f90 -o binaries/x64-linux-sysv-default/Entropy -lyeppp
