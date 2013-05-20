all: Entropy

Entropy: Entropy.f90
	gfortran -O3 -march=native -mtune=native -std=f2003 -I../../sources -L../../../../binaries/linux/x86_64 Entropy.f90 -o Entropy -lyeppp

run: all
	LD_LIBRARY_PATH=${PWD}/../../../../binaries/linux/x86_64 ./Entropy
