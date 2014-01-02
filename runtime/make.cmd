@ECHO off
REM                      Yeppp! library implementation
REM
REM This file is part of Yeppp! library and licensed under the New BSD license.
REM See LICENSE.txt for the full text of the license.

IF "%1" == "clean" GOTO CLEAN
CALL "%~dp0..\make.cmd" %1
GOTO :eof

:CLEAN
RD /S /Q binaries 2>NUL
GOTO :eof