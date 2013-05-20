all: yeplibrary.mod yepcore.mod yepmath.mod

yeplibrary.mod:
	gfortran -std=f2003 -fsyntax-only yepLibrary.f90

yepcore.mod:
	gfortran -std=f2003 -fsyntax-only yepCore.f90

yepmath.mod:
	gfortran -std=f2003 -fsyntax-only yepMath.f90

clean:
	rm -f *.mod
