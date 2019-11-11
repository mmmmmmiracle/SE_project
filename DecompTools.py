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
    def __init__(self, foldername, apk):
        self.foldername = foldername
        self.apk = apk

    def Decompile(self):
        apktool_command = "apktool.jar d " + self.apk + " -o " + self.foldername
        os.system(apktool_command)
    