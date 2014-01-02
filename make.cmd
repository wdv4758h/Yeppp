@ECHO off
REM                      Yeppp! library implementation
REM
REM This file is part of Yeppp! library and licensed under the New BSD license.
REM See LICENSE.txt for the full text of the license.

IF NOT "%2" == "" GOTO ERROR

IF "%1" == "windows-x86" GOTO X86
IF "%1" == "windows-x86_64" GOTO X64
IF "%1" == "generate" GOTO GENERATE
IF "%1" == "clean" GOTO CLEAN
IF "%1" == "help" GOTO HELP
GOTO ERROR

:X86
IF DEFINED VS110COMNTOOLS GOTO VS2012_X86
IF DEFINED VS110COMNTOOLS GOTO VS2010_X86
IF DEFINED VS90COMNTOOLS GOTO VS2008_X86
@ECHO "Could not find Visual Studio 2008, 2010, or 2012"
EXIT /B 1

:X64
IF DEFINED VS110COMNTOOLS GOTO VS2012_X64
IF DEFINED VS110COMNTOOLS GOTO VS2010_X64
IF DEFINED VS90COMNTOOLS GOTO VS2008_X64
@ECHO "Could not find Visual Studio 2008, 2010, or 2012"
EXIT /B 1

:IA64
IF DEFINED VS100COMNTOOLS GOTO VS2010_IA64
IF DEFINED VS90COMNTOOLS GOTO VS2008_IA64
@ECHO "Could not find Visual Studio 2008 or 2010"
EXIT /B 1

:ARM
IF DEFINED VS110COMNTOOLS GOTO VS2012_ARM
@ECHO "Could not find Visual Studio 2012"
EXIT /B 1

:GENERATE
CD "%~dp0" && python "%~dp0codegen/core.py"
CD "%~dp0" && python "%~dp0codegen/math.py"
EXIT /B 0

:CLEAN
RD /S /Q build\linux-x86 2>NUL
RD /S /Q build\linux-x86_64 2>NUL
RD /S /Q build\linux-k1om 2>NUL
RD /S /Q build\linux-armel 2>NUL
RD /S /Q build\linux-armhf 2>NUL
RD /S /Q build\linux-ppc64 2>NUL
RD /S /Q build\linux-bgq 2>NUL
RD /S /Q build\android-armeabi 2>NUL
RD /S /Q build\android-armeabiv7a 2>NUL
RD /S /Q build\android-x86 2>NUL
RD /S /Q build\android-mips 2>NUL
RD /S /Q build\macosx-x86 2>NUL
RD /S /Q build\macosx-x86_64 2>NUL
RD /S /Q build\windows-x86 2>NUL
RD /S /Q build\windows-x86_64 2>NUL
GOTO :eof

:VS2012_X86
SETLOCAL
CALL "%VS110COMNTOOLS%\..\..\VC\vcvarsall.bat" x86
nmake /NOLOGO windows-x86
ENDLOCAL
EXIT /B %ERRORLEVEL%

:VS2012_X64
SETLOCAL
CALL "%VS110COMNTOOLS%\..\..\VC\vcvarsall.bat" x86_amd64
nmake /NOLOGO windows-x86_64
ENDLOCAL
EXIT /B %ERRORLEVEL%

:VS2010_X86
SETLOCAL
CALL "%VS100COMNTOOLS%\..\..\VC\vcvarsall.bat" x86
nmake /NOLOGO windows-x86
ENDLOCAL
EXIT /B %ERRORLEVEL%

:VS2010_X64
SETLOCAL
CALL "%VS100COMNTOOLS%\..\..\VC\vcvarsall.bat" x86_amd64
nmake /NOLOGO windows-x86_64
ENDLOCAL
EXIT /B %ERRORLEVEL%

:VS2008_X86
SETLOCAL
CALL "%VS90COMNTOOLS%\..\..\VC\vcvarsall.bat" x86
nmake /NOLOGO windows-x86
ENDLOCAL
EXIT /B %ERRORLEVEL%

:VS2008_X64
SETLOCAL
CALL "%VS90COMNTOOLS%\..\..\VC\vcvarsall.bat" x86_amd64
nmake /NOLOGO windows-x86_64
ENDLOCAL
EXIT /B %ERRORLEVEL%

:ERROR
ECHO Error: invalid command-line argument(s)
GOTO HELP

:HELP
ECHO Usage: make [param]
ECHO Possible options for [param]
ECHO     windows-x86    - build Yeppp! for 32-bit (x86) Windows
ECHO     windows-x86_64 - build Yeppp! for 64-bit (x86-64 aka x64) Windows
ECHO     clean          - show this help message
ECHO     help           - show this help message
IF "%1" == "help" (
	EXIT /B 0
) ELSE (
	EXIT /B 1
)
