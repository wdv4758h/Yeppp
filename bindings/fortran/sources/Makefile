all: yeplibrary.mod yepcore.mod yepmath.mod

ifeq ($(FC),gfortran)
FFLAGS += -std=f2003
FFLAGS += -fsyntax-only
endif

ifeq ($(FC),ifort)
FFLAGS += -std03
FFLAGS += -syntax-only
endif

yeplibrary.mod:
	$(FC) $(FFLAGS) yepLibrary.f90

yepcore.mod:
	$(FC) $(FFLAGS) yepCore.f90

yepmath.mod:
	$(FC) $(FFLAGS) yepMath.f90

clean:
	rm -f *.mod
