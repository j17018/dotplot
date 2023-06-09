import numpy as np
import re
from PIL import Image,ImageFilter
import cv2

def writeToLog(a):
    with open("log","a") as f:
        f.write(a + "\n")

def readFile(name):
    """
    Example of what this function returns
    ['CGCGACTTTTCGCCCTTTGGCGATCTCCGCTGCCGCGCGTAAATCTTCAATGCGCGAGTTGGTACAGGAACCGATAAACA\n',
    'CTTTGTCGATAGCCACTTCGGTCAGCGGAATACCCGGTTTCAGCCCCATATAGGCCAGCGCTTTTTCTGCCGACGCGCGT\n',
    'TCAACCGGATCGGCAAACGAAGCCGGATCGGGAATATTGTCGTTCACGGAAATCACCTGGCCGGGATTGGTGCCCCAGGT']
    """
    with open(name, "r") as f:
        return f.readlines()

def removeEnter(string):
    return re.sub(r'\n', '', string)

def removeSpace(string):
    return re.sub(r' ', '', string)

#returns the processed string
def processString(file):
    """
    it receives 'CGCGACTTTTCGCCCTTTGGCGATCTCCGCTGCCGCGCGTAAATCTTCAATGCGCGAGTTGGTACAGGAACCGATAAACA\n'
    it is returned without the \n, " "
    """
    file = removeEnter(file)
    file = removeSpace(file)
    return file

#working
def process(arrayB,arrayA,i,j):
    """
    it receives rows and columns and saves the subdotplot of that section
    it saves that subdotplot as an image
    """
    submatrix = np.ones((len(arrayB),len(arrayA)),dtype="bool")
    for k in range(len(arrayB)):
        for w in range(len(arrayA)):
            if arrayB[k] == arrayA[w]:
                submatrix[k][w] = 0
    # print(submatrix)
    # print(i,j)
    # print()
    saveSubDotPlot(submatrix,i,j)

def saveSubDotPlot(numpyArr,i,j):
    im = Image.fromarray(numpyArr)
    im = applyKernelFilter(im)
    im.save("images_subdotplot/sub_{}_{}.jpeg".format(i,j),optimize=True, quality=70)

def countLines(file):
    """
    This runs after you read a file using readFile()
    this returns the amount of lines that the file has minus 1
    because the last one usually is a \n
    """
    return len(file)

def applyKernelFilter(pilImage):
    return pilImage.filter(ImageFilter.Kernel((3, 3),
      (2, 0, 0, 0, 0, 0, 0, 0, 1),1,0))

def rows_save(size,j):
    """
    used in concat_images_usingPool
    """
    imgsAux = [0] * size
    for i in range(size):
        imgsAux[i] = cv2.imread('images_subdotplot/sub_{}_{}.jpeg'.format(j,i))
    cv2.imwrite('images_rows/row{}.jpeg'.format(j), cv2.hconcat(imgsAux[:]))

