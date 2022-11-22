@echo off

rem NUKE
set NUKE_PATH=z:\nuke
set HOME=%NUKE_PATH%\users\%USERNAME%

rem OFX
set OFX_PLUGIN_PATH=\\192.168.50.210\c_$\_appz\OFX
set FOUNDRY_LICENSE_FILE=%OFX_PLUGIN_PATH%/foundry.lic
set FOUNDRY_LICENSE_LOG=%OFX_PLUGIN_PATH%/license.log

rem TEMP
set NUKE_TEMP_DIR=C:\Temp\nuke

"c:\Program Files\Nuke7\Nuke7.0.exe" %*
