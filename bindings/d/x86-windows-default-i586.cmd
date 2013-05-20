set DMD=dmd
set DFLAGS=-c
set CP=copy
set CPFLAGS=/Y
set LIB=lib
set RM=del
set RMFLAGS=/f /s /q
set IMPORT_LIBRARIES=../../runtime/binaries/x86-windows-default-i586/yeprt.lib ../../library/binaries/x86-windows-default-i586/yeppp.lib kernel32.lib

%RM% %RMFLAGS% "binaries/x86-windows-default-i586" >NUL 2>NUL
mkdir "binaries/x86-windows-default-i586/" >NUL 2>NUL
mkdir "binaries/x86-windows-default-i586/yeppp" >NUL 2>NUL

%DMD% %DFLAGS% -ofbinaries/x86-windows-default-i586/yeppp/library.obj sources/yeppp/library.d

%LIB% -c -p32 binaries/x86-windows-default-i586/yeppp-d.lib binaries/x86-windows-default-i586/yeppp/library.obj
