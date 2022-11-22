@echo off

rem NUKE
set NUKE_PATH=z:\nuke
set HOME=%NUKE_PATH%\users\%USERNAME%

rem OFX
rem set OFX_PLUGIN_PATH=
rem set FOUNDRY_LICENSE_FILE=
rem set FOUNDRY_LICENSE_LOG=

rem TEMP
set NUKE_TEMP_DIR=C:\Temp\nuke

"c:\Program Files\Nuke6.3v8\Nuke6.3.exe" %*
