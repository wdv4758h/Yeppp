set CXX=cl
set CXXFLAGS=/nologo /Zl /GS- /EHs- /GR- /I../../library/headers /Isources-jni "/I%JAVA_HOME%/include" "/I%JAVA_HOME%/include/win32" /Oi /c
set CP=copy
set CPFLAGS=/Y
set RM=del
set RMFLAGS=/f /s /q
set IMPORT_LIBRARIES=../../runtime/binaries/x64-windows-ms-default/yeprt.lib ../../library/binaries/x64-windows-ms-default/yeppp.lib kernel32.lib

%RM% %RMFLAGS% "binaries/x64-windows-ms-default" >NUL 2>NUL
mkdir "binaries/x64-windows-ms-default/" >NUL 2>NUL
mkdir "binaries/x64-windows-ms-default/core" >NUL 2>NUL
mkdir "binaries/x64-windows-ms-default/library" >NUL 2>NUL
mkdir "binaries/x64-windows-ms-default/math" >NUL 2>NUL

%CXX% /O1 %CXXFLAGS% /Fobinaries/x64-windows-ms-default/core/ sources-jni/core/*.c

%CXX% /O1 %CXXFLAGS% /Fobinaries/x64-windows-ms-default/math/ sources-jni/math/*.c

%CXX% /O1 %CXXFLAGS% /Fobinaries/x64-windows-ms-default/library/ sources-jni/library/*.c

rc /I../../library/headers /Fobinaries/x64-windows-ms-default/library/Version.res sources-jni/library/Version.rc

link /nologo /NODEFAULTLIB /DLL /MACHINE:X64 /OUT:binaries/x64-windows-ms-default/yeppp-jni.dll binaries/x64-windows-ms-default/core/*.obj binaries/x64-windows-ms-default/math/*.obj binaries/x64-windows-ms-default/library/*.obj binaries/x64-windows-ms-default/library/Version.res %IMPORT_LIBRARIES%

%CP% %CPFLAGS% "binaries\x64-windows-ms-default\yeppp-jni.dll" "..\..\binaries\windows\amd64\yeppp-jni.dll" >NUL 2>NUL
