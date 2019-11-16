@echo off
echo *************************************
echo Start Extract
echo *************************************
cd /d %1

if EXIST %2 (
    goto 1
) else (
    goto 0
)

:0
echo failed
pause

:1
goto edit

:edit
cd /d %2

if EXIST /d %1\%2\newPmsnAlys.txt(
    del newPmsnAlys.txt
)

for /f "delims=" %%a in (AndroidManifest.xml) do (
    echo "%%a"|find "android.permission" && echo %%a >> newPmsnAlys.txt
)

cd ..
echo *************************************
echo End
echo *************************************

