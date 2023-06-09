"""
This code generates images used to make a dotplot given two dna sequences

This implementation requires that the 2 files have equal amount of lines and that
each line has the same amount of elements 
(it has not been tested otherwise)
"""

import numpy as np
import matplotlib.pyplot as plt
import re
import time
from PIL import Image
import cv2
import argparse
import sys
import subprocess
from functionsShared import *
from multiprocessing import Pool

# sizeOfSequences = 80*200

"""
clean images_subdotplot
"""
subprocess.call('sudo rm images_subdotplot/ -R', shell=True)
subprocess.call('mkdir images_subdotplot', shell=True)

"""
Constants
"""
SIZE = ""
CORES = 0
"""
let the user choose the size of lines in each sequence

let the user put the name of the files
"""

parser = argparse.ArgumentParser()

parser.add_argument("file1")
parser.add_argument("file2")
parser.add_argument("size")
parser.add_argument("cores")

args = parser.parse_args()
totaltime = time.time()
start = time.time()

try:
    file1 = readFile(args.file1)
    file2 = readFile(args.file2)
except:
    print("Verify that the names of the files are correct")
    sys.exit()

try:
    SIZE = int(args.size)
    """
    it returns the N elements, if the user wants to compare the first 100, or 200, or N value
    """
    file1 = file1[:SIZE]
    file2 = file2[:SIZE]
except:
    print("Verify that the lines size can be fitted into both sequences, remember it needs to be the same for both files")
    sys.exit()
try:
    CORES = int(args.cores)
except:
    print("In cores enter a number")
    sys.exit()
if CORES <= 0:
    print("In cores enter a number greater than zero")
    sys.exit()
"""
file1 and file2 has the same amount of lines and elements in each line
"""
writeToLog("number of cores {}".format(CORES))

writeToLog("lines size {}".format(SIZE))

pool = Pool(processes=CORES)

for i in range(len(file2)):
    for j in range(len(file1)):

        if len(file2[i]) == 1 or len(file1[j]) == 1:
            """
            dont compare strings with "\n" elements or only one element
            thats what that if does
            """
            break
        pool.apply_async(process,(processString(file2[i]),processString(file1[j]),i,j))
pool.close()
pool.join()

aux1 = time.time()
print("ellapsed making the subplots",aux1-start)
writeToLog("ellapsed making the subplots {}".format(aux1-start))

subprocess.run(["python3", "concat_images.py", str(SIZE),str(CORES)])

aux2 = time.time()
print("ellapsed total time",aux2-totaltime)
writeToLog("ellapsed total time {}".format(aux2-totaltime))

res = subprocess.run(["du", "-h", "-s"],capture_output=True,text=True)#file size of all the directory
print("size of all the folder {}".format(res.stdout))
writeToLog("size of all the folder {}".format(res.stdout))
writeToLog("")

