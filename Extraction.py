#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

class Extracter():
    def __init__(self, folderName, folderPath):
        self.folderName = folderName
        self.folderPath = folderPath
        self.fileName = folderName

    def Save2File(self, resultPath, extFileName, contents):
        # Write contents in the end of the file
        filePath = resultPath + "\\result\\" + extFileName
        fh = open(filePath, 'a')
        fh.write(contents)
        fh.close()

    def GetMainfest(self):
        # Get the current working directory
        DstDir = os.getcwd()
        path1 = DstDir + "\\decompileResult"
        #path2 = "decompileResult\\" + self.folderName
        # Get manifest
        os.system('extractManifest.bat %s %s' % (path1, self.folderName))
        command = "copy " + DstDir + "\\decompileResult\\" + self.folderName + "\\newPmsnAlys.txt" + " " + DstDir
        os.system(command)
        print("+==================================+")
        print("The command is: ", command)
        print("The current cwd is:", os.getcwd())
        print("+==================================+")

    def ExtractFile(self):
        # Get the current working directory
        DstDir = os.getcwd()
        outputName = self.fileName + ".txt"
        with open(r"newPmsnAlys.txt") as f:
            for line in f.readlines():
                m = line.split('=')
                m1 = m[-1]
                m2 = m1[1:-5]
                m3 = m2.split('.')
                result = m3[-1]
                self.Save2File(DstDir, outputName, "%s\n\r" % result)
        os.remove("newPmsnAlys.txt")
    


