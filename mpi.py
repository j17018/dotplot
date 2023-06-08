from mpi4py import MPI
import numpy as np
import matplotlib.pyplot as plt
import re
import time
import os

def calculate_dotplot(file1, file2, start_row, end_row, section_path):
    with open(section_path, 'a') as f:
        for i in range(start_row, end_row):
            row = []
            for j in range(len(file2)):
                if file1[i] == file2[j]:
                    f.write('*')
                else:
                    f.write(' ')
            f.write('\n')

def readFile(name):
    with open(name, "r") as f:
        return f.read()

def removeEnter(string):
    return re.sub(r'\n', '', string)

def removeEmpty(string):
    return re.sub(r'', '', string)

def removeSpace(string):
    return re.sub(r' ', '', string)

def processFile(file):
    file = removeEnter(file)
    file = removeEmpty(file)
    file = removeSpace(file)
    return file

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if rank == 0:
        file1 = readFile("E_coli.fna")
        file1 = processFile(file1)

        file2 = readFile("Salmonella.fna")
        file2 = processFile(file2)

        # Determine the number of rows per process
        rows_per_process = int(np.ceil(len(file1) / size))

        # Distribute the data to all processes
        file1 = comm.bcast(file1, root=0)
        file2 = comm.bcast(file2, root=0)
    else:
        file1 = None
        file2 = None
        rows_per_process = None

    # Scatter the rows to different processes
    local_rows = comm.scatter(file1, root=0)

    # Determine the start and end row for each process
    start_row = rank * rows_per_process
    end_row = min((rank + 1) * rows_per_process, len(local_rows))

    # Perform the dotplot calculation locally
    section_path = f'dotplot_section_{rank}.txt'
    calculate_dotplot(local_rows, file2, start_row, end_row, section_path)

    # Gather the section paths from all processes
    section_paths = comm.gather(section_path, root=0)

    if rank == 0:
        # Join all dotplot sections into one file
        output_path = 'dotplot_complete.txt'
        with open(output_path, 'w') as f:
            for section_path in section_paths:
                with open(section_path, 'r') as section_file:
                    for line in section_file:
                        f.write(line)

        # Clean up section files
        for section_path in section_paths:
            os.remove(section_path)

if __name__ == '__main__':
    start = time.time()
    main()
    print("Elapsed time:", time.time() - start)