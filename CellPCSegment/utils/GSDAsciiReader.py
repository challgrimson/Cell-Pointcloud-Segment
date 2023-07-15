# Reads GSD Microscopy Ascii files.

import numpy as np
import csv 

#its just comma delimited so CSV
class GSDAsciiReader:

    def __init__(self, xColIndex=3, yColIndex=4):
        self.xColIndex = xColIndex
        self.yColIndex = yColIndex

    def read(self, path):
        assert (path[-6:] == '.ascii'), 'Not an ascii file'
        
        mat = []
        with open(path, newline='') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',')
            next(csvreader) #skip header
            for row in csvreader:
                mat.append([float(row[self.xColIndex])*99, float(row[self.yColIndex])*99])
                
        return np.array(mat)
        