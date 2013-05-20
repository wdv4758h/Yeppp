set CXX=cl
set CXXFLAGS=/nologo /Zl /GS- /EHs- /GR- /I../../library/headers /Isources-jni "/I%JAVA_HOME%/include" "/I%JAVA_HOME%/include/win32" /Oi /c
set CP=copy
set CPFLAGS=/Y
set RM=del
set RMFLAGS=/f /s /q
set IMPORT_LIBRARIES=../../runtime/binaries/x86-windows-default-i586/yeprt.lib ../../library/binaries/x86-windows-default-i586/yeppp.lib kernel32.lib

%RM% %RMFLAGS% "binaries/x86-windows-default-i586" >NUL 2>NUL
mkdir "binaries/x86-windows-default-i586/" >NUL 2>NUL
mkdir "binaries/x86-windows-default-i586/core" >NUL 2>NUL
mkdir "binaries/x86-windows-default-i586/library" >NUL 2>NUL
mkdir "binaries/x86-windows-default-i586/math" >NUL 2>NUL

%CXX% /O1 %CXXFLAGS% /Fobinaries/x86-windows-default-i586/core/ sources-jni/core/*.c

%CXX% /O1 %CXXFLAGS% /Fobinaries/x86-windows-default-i586/math/ sources-jni/math/*.c

%CXX% /O1 %CXXFLAGS% /Fobinaries/x86-windows-default-i586/library/ sources-jni/library/*.c

rc /I../../library/headers /Fobinaries/x86-windows-default-i586/library/Version.res sources-jni/library/Version.rc

link /nologo /NODEFAULTLIB /DLL /MACHINE:X86 /OUT:binaries/x86-windows-default-i586/yeppp-jni.dll binaries/x86-windows-default-i586/core/*.obj binaries/x86-windows-default-i586/math/*.obj binaries/x86-windows-default-i586/library/*.obj binaries/x86-windows-default-i586/library/Version.res %IMPORT_LIBRARIES%

%CP% %CPFLAGS% "binaries\x86-windows-default-i586\yeppp-jni.dll" "..\..\binaries\windows\x86\yeppp-jni.dll" >NUL 2>NUL
