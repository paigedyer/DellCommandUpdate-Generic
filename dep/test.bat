@echo off

Rem This script is to transfer the installation file for DCU to the user's computer

xcopy /f "\\pbovpfsmb01\install\commandupdate\DCU_SETUP_4_3_0.EXE" "C:\Windows" /Y /I
xcopy /f "C:\Windows\{34647E6A-01F8-4BED-97D9-5E83CA5EAC07}" "C:\Windows" /Y /I

