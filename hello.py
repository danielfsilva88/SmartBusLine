# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 19:24:38 2017

@author: gabri
"""
from utils.utils import readNodesJsonFile, parseJsonString
# Demo file for Spyder Tutorial
# Hans Fangohr, University of Southampton, UK


def hello():
    """Print "Hello World" and return None"""
    print("Laters World")

# main program starts here
hello()
jsonString = readNodesJsonFile()
nodes = parseJsonString(jsonString)
print (nodes)
