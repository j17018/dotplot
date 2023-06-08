import concurrent.futures
import numpy as np
import matplotlib.pyplot as plt
import re
import time

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
    # Assuming you have already loaded the sequences from "file1" and "file2" into variables
    file1 = readFile("E_coli.fna")
    file1 = processFile(file1)

    file2 = readFile("Salmonella.fna")
    file2 = processFile(file2)

    # Determine the number of CPU cores to use
    num_cores = 6

    # Determine the chunk size for each core
    chunk_size = int(np.ceil(len(file1) / num_cores))

    # Set up the ProcessPoolExecutor with the specified number of cores
    executor = concurrent.futures.ProcessPoolExecutor(max_workers=num_cores)

    # Submit the dotplot calculation to the executor for each chunk
    futures = []
    section_paths = []
    for i in range(0, len(file1), chunk_size):
        start = i
        end = min(i + chunk_size, len(file1))
        section_path = f'dotplot_section_{i}.txt'
        future = executor.submit(calculate_dotplot, file1, file2, start, end, section_path)
        futures.append(future)
        section_paths.append(section_path)

    # Wait for all futures to complete
    concurrent.futures.wait(futures)

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
