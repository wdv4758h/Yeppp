set JAVAC=javac
set JAVAFLAGS=-classpath sources-java -d binaries/java-1.5 -target 1.5
set CP=copy
set CPFLAGS=/Y
set RM=del
set RMFLAGS=/f /s /q
set MKDIR=mkdir
set MKDIRFLAGS=

%RM% %RMFLAGS% "binaries/java-1.5" >NUL 2>NUL
%MKDIR% %MKDIRFLAGS% "binaries/java-1.5/" >NUL 2>NUL

%JAVAC% %JAVAFLAGS% sources-java/info/yeppp/SystemException.java

%JAVAC% %JAVAFLAGS% sources-java/info/yeppp/MisalignedPointerError.java

%JAVAC% %JAVAFLAGS% sources-java/info/yeppp/UnsupportedHardwareException.java

%JAVAC% %JAVAFLAGS% sources-java/info/yeppp/UnsupportedSoftwareException.java

%JAVAC% %JAVAFLAGS% sources-java/info/yeppp/Core.java

%JAVAC% %JAVAFLAGS% sources-java/info/yeppp/Library.java

%JAVAC% %JAVAFLAGS% sources-java/info/yeppp/Math.java

%JAVAC% %JAVAFLAGS% sources-java/info/yeppp/Version.java

%JAVAC% %JAVAFLAGS% sources-java/info/yeppp/CpuArchitecture.java

%JAVAC% %JAVAFLAGS% sources-java/info/yeppp/CpuVendor.java

%JAVAC% %JAVAFLAGS% sources-java/info/yeppp/CpuMicroarchitecture.java

%JAVAC% %JAVAFLAGS% sources-java/info/yeppp/CpuIsaFeature.java

%JAVAC% %JAVAFLAGS% sources-java/info/yeppp/CpuCycleCounterState.java

%JAVAC% %JAVAFLAGS% sources-java/info/yeppp/ArmCpuIsaFeature.java

%JAVAC% %JAVAFLAGS% sources-java/info/yeppp/X86CpuIsaFeature.java

%JAVAC% %JAVAFLAGS% sources-java/info/yeppp/IA64CpuIsaFeature.java

%JAVAC% %JAVAFLAGS% sources-java/info/yeppp/MipsCpuIsaFeature.java

%JAVAC% %JAVAFLAGS% sources-java/info/yeppp/CpuSimdFeature.java

%JAVAC% %JAVAFLAGS% sources-java/info/yeppp/ArmCpuSimdFeature.java

%JAVAC% %JAVAFLAGS% sources-java/info/yeppp/X86CpuSimdFeature.java

%JAVAC% %JAVAFLAGS% sources-java/info/yeppp/MipsCpuSimdFeature.java

%JAVAC% %JAVAFLAGS% sources-java/info/yeppp/CpuSystemFeature.java

%JAVAC% %JAVAFLAGS% sources-java/info/yeppp/ArmCpuSystemFeature.java

%JAVAC% %JAVAFLAGS% sources-java/info/yeppp/X86CpuSystemFeature.java

jar cf binaries/java-1.5/yeppp.jar -C binaries/java-1.5/ info/yeppp

%CP% %CPFLAGS% "binaries\java-1.5\yeppp.jar" "..\..\binaries\java-1.5\yeppp.jar" >NUL 2>NUL
