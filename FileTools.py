#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  25 14:13:25 2019

@author: 刘懿
"""

import sys
import os
import re

class File():
    """
    To processing files
    """
    def __init__(self, argv):
        self.argv = argv

    def IsApkFile(self, dir): 
        s = dir[-4:]
        return s == ".apk"

    def GetFilePath(self, dir):
        """
        Get file path
        """
        fileList = []
        for home, dirs, files in os.walk(dir):
            for filename in files:
                if self.IsApkFile(filename):
                    file_path = os.path.join(home, filename)
                    fileList.append(file_path)
                    print(file_path)
                else:
                    continue
                    print("Not a .apk file")
        return fileList

    def GetFileList(self):
        '''
        Get the path of files
        '''
        if len(self.argv) > 1:
            rootPath = self.GetFilePath(self.argv[1])
        else:
            arg1 = input("please input apk file path:\n")
            rootPath = self.GetFilePath(arg1)
        return rootPath

    def RetFinPathByCmd(self):
        '''
        Return the dex file path
        '''
        pathList = self.GetFileList()
        dexPath = pathList[0]
        if dexPath == "":
            print("--Fail-- Return file path ")
            exit(-1)
        print("--Sucs-- Return file path ")
        return pathList

    def LoopDirFiles(self, path, fileList, keyStr, lens):
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
                self.LoopDirFiles(filePath, fileList, keyStr, lens)
            else:
                strLen = len(filePath)
                # Get the .apk files
                if filePath[(strLen-lens):strLen] == keyStr:
                    fileList.append(filePath)