""" This script takes any number of repeats of EUV IRs, return the
STDEV of 2x2 for all defects caught 100% across repeats
"""
import sys
from glob import glob
import re

def read_ir(*args):
    """ read IR.txt, map the 2x2 to the defect coordinate, and
    save the information in a dictionary;
    Take any number (>1) of IRs, save the final result in a list
    defect residue <80

    Input: ir.txt 
    Output: a list of dictionary [{'coord':(2x2)},{},...]
    """
    
    DOI=[]
    
    for arg in args:
        fin = open(arg,"r")
        res = dict()
    
        for line in fin:
            if re.search('LEOrCorner.*PassIdx', line):
                coord = re.findall('Location: ([0-9.]+\s?,\s?[0-9.]+) mm',line)
                x = (coord[0].split(',')[0].strip())[:-4]
                y = (coord[0].split(',')[1].strip())[:-4]
                location = x + ',' + y

                residue = re.findall('Descr: \(2x2=(\S*),', line)
                #detector = re.findall('Type: (\S+)\s+Class', line)
                
            # Only consider defect with 2x2 < 80 gs
                if float(residue[0]) < 80:
                    #defect = (residue[0], detector[0])
                
            # Build a dictionary where 'DOI coord:key', 'DOI 2x2: value'
                    res[location] = residue[0]
                
        DOI.append(res)
        fin.close()

    return (DOI)

def DOI_full_list(DOI):
    """input: read_ir [{},{},...]
    output: full_list_dict {key1:[], key2:[],...}
    """

    common_DOI = set.intersection(*map(set, DOI))
    full_list_dict = {}

    for key in common_DOI:
        residue_list = []
        for d in DOI:
            residue_list.append(d[key])
        full_list_dict[key] = residue_list

    return full_list_dict
    
def STDEV(s):
    """ calculate the max, min, average, and standard deviation
    of a given list of numbers.

    input: list of float 
    output: float
    """
    import math

    def average(s):
        return sum(s)*1.0/len(s)
    
    ave = average(s)
    variance = list(map(lambda x: (x-ave)**2, s))
    DEV = math.sqrt(average(variance))

    result = [max(s), min(s), ave, round(DEV,2)*3] + s

    return result
        
def DOI_STDEV(full_list):

    res = dict()
    for key in full_list:
        # convert the str residue to float residue
        float_num = list(map(lambda x: float(x), full_list[key]))

        res[key]= STDEV(float_num)
        
        #for item in full_list[key]:
            #res[key].append(item[1])

    #return {'coord': (max, min, average, 3xSTDEV, rpt1, rpt2, rpt3 ...*)}

    return res

def write_file(res,args):
    """ input is result from DOI_STDEV, and full_list from DOI_full_list
    output is csv file
    """
    
    fout=open('EUV.csv','w')

    num_rpt = len(args)
    fout.write("X mm, Y mm, max2x2, min2x2, ave2x2, 3xSTDEV2x2,")

    for i in range(num_rpt):
        fout.write("rpt%d,"%(i+1))

    fout.write("\n")
    
    for k in res:        
        string = str(k) + ',' +(str(res[k]))[1:-1] + '\n'
        fout.write(string)
    
    fout.close()

def main():

    args = glob(input("Please provide txt IRs: \n"))
    print ('Total %s IRs are provided'%len(args))
    DOI = read_ir(*args)
    full_list = DOI_full_list(DOI)
    result = DOI_STDEV(full_list)
    write_file(result,args)

if __name__ == '__main__':
    main()

