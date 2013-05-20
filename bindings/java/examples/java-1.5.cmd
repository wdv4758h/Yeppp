set JAVAC=javac
set JAVACFLAGS=-classpath ../binaries/java-1.5/yeppp.jar -d binaries -target 1.5
set RM=del
set RMFLAGS=/f /s /q
set MKDIR=mkdir
set MKDIRFLAGS=

%RM% %RMFLAGS% "binaries/java" >NUL 2>NUL
%MKDIR% %MKDIRFLAGS% "binaries/java/" >NUL 2>NUL

%JAVAC% %JAVACFLAGS% sources/Entropy.java

@cmd /C "set PATH=%CD%/../../../library/binaries/x64-windows-ms-default;%CD%/../binaries/x64-windows-ms-default;%PATH% && java -classpath ../binaries/java-1.5/yeppp.jar;binaries Entropy"

%JAVAC% %JAVACFLAGS% sources/CpuInfo.java

@cmd /C "set PATH=%CD%/../../../library/binaries/x64-windows-ms-default;%CD%/../binaries/x64-windows-ms-default;%PATH% && java -classpath ../binaries/java-1.5/yeppp.jar;binaries CpuInfo"

%JAVAC% %JAVACFLAGS% sources/CpuCycles.java

@cmd /C "set PATH=%CD%/../../../library/binaries/x64-windows-ms-default;%CD%/../binaries/x64-windows-ms-default;%PATH% && java -classpath ../binaries/java-1.5/yeppp.jar;binaries CpuCycles"

%JAVAC% %JAVACFLAGS% sources/SystemTimer.java

@cmd /C "set PATH=%CD%/../../../library/binaries/x64-windows-ms-default;%CD%/../binaries/x64-windows-ms-default;%PATH% && java -classpath ../binaries/java-1.5/yeppp.jar;binaries SystemTimer"
