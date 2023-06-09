import cv2
import time
import argparse
import subprocess
from functionsShared import writeToLog,rows_save
from multiprocessing import Pool
"""
clean images_rows
"""
subprocess.call('sudo rm images_rows/ -R', shell=True)
subprocess.call('mkdir images_rows', shell=True)

parser = argparse.ArgumentParser()
parser.add_argument("size")
parser.add_argument("cores")
args = parser.parse_args()

"""
join all rows
"""
#importante, este valor asume que la secuencia A y B deben tener la misma cantidad de elementos
size = int(args.size)
CORES = int(args.cores)

start = time.time()

imgs = [0] * size

pool = Pool(processes=CORES)

for j in range(size):
    pool.apply_async(rows_save,(size,j))
    
pool.close()
pool.join()

aux1 = time.time()
print("ellapsed making all rows",aux1-start)
writeToLog("ellapsed making all rows {}".format(aux1-start))

"""
join all rows into one image, this image is the final dotplot
"""
start = time.time()

for i in range(size):
    imgs[i] = cv2.imread('images_rows/row{}.jpeg'.format(i))
cv2.imwrite('dotplot_final.jpeg', cv2.vconcat(imgs[:]))



aux2 = time.time()
print("ellapsed joining all rows, making the final dotplot",time.time()-start)
writeToLog("ellapsed joining all rows, making the final dotplot {}".format(aux2-start))

"""
show all the files sizes
"""

res2 = subprocess.run(['ls' ,'-l'],capture_output=True,text=True)
writeToLog(str(res2.stdout))
