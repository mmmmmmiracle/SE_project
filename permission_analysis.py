#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  25 14:13:25 2019

@author: 刘懿
"""

import sys
import os
import re
import random

def GetFilePath():
    """
    Get file path
    """
    list = []
    if len(sys.argv) > 1:
        list.append(sys.argv[1])
    else:
        arg1 = input("please input apk file path:\n")
        list.append(arg1)
    return list


def RetDexPathByCmd():
    """
    Return the file path
    """
    listArgv = GetFilePath()
    dexPath = listArgv[0]
    if dexPath == "":
        print("--Fail-- Return file path ")
        exit(-1)
    print("--Sucs-- Return file path ")
    return dexPath


def LoopDirFiles(path, fileList, keyStr, lens):
    """
    Loop dir and get the path of the .apk files
    """
    # Return the list of files and directories in the path
    files = os.listdir(path)
    # loop all the files
    for file in files:
        # Concat the file path
        filePath = os.path.join(path, file)
        # If the path is directory, loop this dir
        if os.path.isdir(filePath):
            LoopDirFiles(filePath, fileList, keyStr, lens)
        else:
            strLen = len(filePath)
            # Get the .apk files
            if filePath[(strLen-lens):strLen] == keyStr:
                fileList.append(filePath)


def GetSaltTimeStr():
    """
    Get the start time
    """
    return time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + str(random.randint(0, 99999999))


def Decomplier(foldername):
    """
    Decomply the .apk file
    """
    apktool_command = "apktool.jar d " + apk + " -o " + foldername
    # print(apktool_command)
    os.system(apktool_command)

def Save2File(file_name, contents):
    # Write contents in the end of the file
    fh = open(file_name, 'a')
    fh.write(contents)
    fh.close()


if __name__ == "__main__":
    print("-------------- Start Main Function --------------")
    # Delete the exist files
    if(os.path.exists("newPmsnAlys.txt")):
        os.remove("newPmsnAlys.txt")
    if (os.path.exists("APIextraction.txt")):
        os.remove("APIextraction.txt")
    # Get all path list:
    apkPath = RetDexPathByCmd()

    # Get the .apk file path list
    apkList = []
    if os.path.isdir(apkPath):
        # Loop all the files
        LoopDirFiles(apkPath, apkList, ".apk", 4)
    else:
        strLen = len(apkPath)
        if apkPath[strLen - 4:strLen] == ".apk":
            apkList.append(apkPath)

    for file in apkList:
        # Split the file path and get the filename
        str = re.split(r"\\", file)
        apk = str[-1]
        folderName = apk[0:-4]
        # print(apk)

        # Decomplier file and get smali, manifest
        if (os.path.exists(folderName)):
            print("The %s is exist, continue" % (folderName))
        else:
            Decomplier(folderName)

        # Get the current working directory
        DstDir = os.getcwd()
        # print(DstDir)

        # Get manifest
        os.system('extractManifest.bat %s' % (folderName))
        # Get smali path
        os.system('api.bat %s' % (folderName))
        command = "copy " + DstDir + "\\" + apk + "\\newPmsnAlys.txt" + " " + DstDir
        # print(command)
        command2 = "copy " + DstDir + "\\" + apk + "\\smali\\smaliFileList.txt" + " " + DstDir
        # print(command2)
        os.system(command)
        os.system(command2)
        # print(os.getcwd())

        # Extraction the permission
        with open(r"newPmsnAlys.txt") as f:
            for line in f.readlines():
                m = line.split('=')
                m1 = m[-1]
                m2 = m1[1:-5]
                m3 = m2.split('.')
                result = m3[-1]
                Save2File('ManifestExtraction.txt', "%s\n\r" % result)

        os.remove("newPmsnAlys.txt")