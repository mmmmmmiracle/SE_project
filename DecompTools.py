#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  25 14:13:25 2019

@author: 刘懿
"""

import sys
import os
import re

class Decompiler():
    """
    Decomply the .apk file
    """
    def __init__(self, foldername, path):
        self.foldername = foldername
        self.path = path

    def Decompile(self):
        dir = os.getcwd()
        print("The current dir before decompile is: ", dir)
        apktool_command = "apktool.jar d " + self.path + " -o decompileResult\\" + self.foldername
        os.system(apktool_command)
    