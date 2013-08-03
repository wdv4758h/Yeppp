@ECHO off
REM                      Yeppp! library implementation
REM
REM This file is part of Yeppp! library and licensed under the New BSD license.
REM See library/LICENSE.txt for the full text of the license.

IF NOT "%2" == "" GOTO error

IF "%1" == ""    GOTO detect
IF "%1" == "x86" GOTO x86
IF "%1" == "x64" GOTO x64
IF "%1" == "/?"  GOTO help
GOTO error

:detect
IF /i %PROCESSOR_ARCHITECTURE% == AMD64 GOTO x64
IF /i %PROCESSOR_ARCHITEW6432% == AMD64 GOTO x64
IF /i %PROCESSOR_ARCHITECTURE% == x86 GOTO x86
ECHO Error: unknown system architecture %processor_architecture%
GOTO help

:x86
SET YEPROOT=%~dp0
SET PATH=%YEPROOT%binaries\windows\x86;%PATH%
IF EXIST %YEPROOT%binaries\clr-2.0\yeppp-clr.dll SET PATH=%YEPROOT%binaries\clr-2.0;%PATH%
IF EXIST %YEPROOT%binaries\java-1.5\yeppp.jar SET CLASSPATH=%YEPROOT%binaries\java-1.5\yeppp.jar;%CLASSPATH%
EXIT /B 0

:x64
SET YEPROOT=%~dp0
SET PATH=%YEPROOT%binaries\windows\x64;%PATH%
IF EXIST %YEPROOT%binaries\clr-2.0\yeppp-clr.dll SET PATH=%YEPROOT%binaries\clr-2.0;%PATH%
IF EXIST %YEPROOT%binaries\java-1.5\yeppp.jar SET CLASSPATH=%YEPROOT%binaries\java-1.5\yeppp.jar;%CLASSPATH%
EXIT /B 0

:error
ECHO Error: invalid command-line argument(s)
GOTO help

:help
ECHO Usage: SetVars.cmd [param]
ECHO Possible options for [param]
ECHO     x86 - set variables for 32-bit (x86) environment
ECHO     x64 - set variables for 64-bit (x86-64 aka x64) environment
ECHO.    /?  - show this help message
ECHO If neither option is specified, the variable are set based on OS architecture.
IF "%1" == "/?" EXIT /B 0
ELSE EXIT /B 1
