set CSC=csc
set CSCFLAGS=/nologo /optimize+ /target:exe /unsafe /reference:..\binaries\yeppp-clr.dll
set CP=copy
set CPFLAGS=/Y
set RM=del
set RMFLAGS=/f /s /q
set MKDIR=mkdir
set MKDIRFLAGS=

%RM% %RMFLAGS% "binaries" >NUL 2>NUL
%MKDIR% %MKDIRFLAGS% "binaries" >NUL 2>NUL

%CSC% %CSCFLAGS% /out:binaries/Entropy.exe sources\Entropy.cs

%CP% %CPFLAGS% ..\binaries\yeppp-clr.dll binaries\yeppp-clr.dll >NUL 2>NUL
