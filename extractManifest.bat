@echo off
cd /d %~dp0


if EXIST %1 goto 1
else goto 0


:0

echo failed
pause

:1
goto edit

:edit
cd %1

IF EXIST /d %~dp0\newPmsnAlys.txt(
del newPmsnAlys.txt
)

for /f "delims=" %%a in (AndroidManifest.xml) do (
echo "%%a"|find "android.permission" &&echo %%a >>newPmsnAlys.txt
)
cd ..
echo end...

