@echo off
cd /d %~dp0

cd %1/smali

IF EXIST /d %~dp0\smaliFileList.txt(
del smaliFileList.txt
)
dir /a-d /b /s *.smali>smaliFileList.txt
 
cd ..
cd ..
