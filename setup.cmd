@echo off
rem BDSP PC rebuild - one-command project setup. Usage: setup.cmd [-Dump <folder with exefs and romfs>] (details: setup\bootstrap.ps1)
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0setup\bootstrap.ps1" %*
exit /b %ERRORLEVEL%
