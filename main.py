#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  25 14:13:25 2019

@author: 刘懿
"""

import os
import re
import sys
from DecompTools import Decompiler
from FileTools import File
from Extraction import Extracter

def main():
    print("-------------- Start Main Function --------------")
    
    # Delete the exist files        ***
    if(os.path.exists("newPmsnAlys.txt")):
        os.remove("newPmsnAlys.txt")

    # The file tool
    fileTool = File(sys.argv)

    # Get all path list:
    apkList = fileTool.RetFinPathByCmd()

    for path in apkList:
        # Split the file path and get the filename
        str = re.split(r"\\", path)
        apk = str[-1]

        folderName = re.split(r"/", apk)[-1][0:-4]
        folderPath = apk[0:-4]

        print("+==================================+")
        print("The path is: ", path)
        print("The str is: ", str)
        print("apk is: ", apk)
        print("folderName is: ", folderName)
        print("folderPath is: ", folderPath)
        print("+==================================+")

        # Decomplier file and get manifest
        if (os.path.exists(folderName)):
            print("The %s is exist, continue" % (folderPath))
        else:
            dec = Decompiler(folderName, path)
            dec.Decompile()

        # Create an Extracter
        extracter = Extracter(folderName, folderPath)

        # Get manifest
        extracter.GetMainfest()

        # Extraction the permission
        extracter.ExtractFile()

if __name__ == "__main__":
    main()
