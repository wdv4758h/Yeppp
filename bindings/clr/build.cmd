set CSC=csc
set CSCFLAGS=/nologo /optimize+ /target:library /unsafe
set CP=copy
set CPFLAGS=/Y
set RM=del
set RMFLAGS=/f /s /q
set MKDIR=mkdir
set MKDIRFLAGS=

%RM% %RMFLAGS% "binaries" >NUL 2>NUL
%MKDIR% %MKDIRFLAGS% "binaries" >NUL 2>NUL

rc /I../../library/headers /Fobinaries/Version.res sources-csharp/Version.rc

%CSC% %CSCFLAGS% /out:binaries/yeppp-clr.dll /win32res:binaries/Version.res sources-csharp\library\*.cs sources-csharp\math\*.cs sources-csharp\core\*.cs

%CP% %CPFLAGS% "binaries\yeppp-clr.dll" "..\..\binaries\clr-2.0\yeppp-clr.dll" >NUL 2>NUL
