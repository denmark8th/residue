""" This script takes two CSVs from RPI_rpt.py, return the
common defects of these two.
"""

def read_csv(csv):
    """ read the csv file and generate dictionary of
    {(x,y):(data)}
    """

    with open(csv, "r+") as fin:

        res = {}
        for line in fin:
            ls = line.split(',')
            coord = (ls[0],ls[1])
            data = list(map(float,ls[2:11]))
            res[coord] = data
        
    return res

def full_list(res1, res2):
    """input: res1, res2 from read_csv
    output: full_list_dict {coord1:[data1,data2], coord2:[data1,data2],...}
    """
    
    # python 3 code:
    common_DOI = set(res1).intersection(set(res2))
        
    DOI_list = {}

    for key in common_DOI:
        DOI_list[key] = res1[key] + res2[key]
    
    return DOI_list

def write_file(DOI_list):
    """ input is result from full_list
    output is csv file
    """
    
    fout=open('EUV-combine.csv','w')
    fout.write("X mm, Y mm, 1max2x2, 1min2x2, 1ave2x2, 3xSTDEV2x2, 1rpt1, 1rpt2, 1rpt3, 1rpt4, 1rpt5,")
    fout.write("2max2x2, 2min2x2, 2ave2x2, 3xSTDEV2x2, 2rpt1, 2rpt2, 2rpt3, 2rpt4, 2rpt5 \n")
    
    for k in DOI_list:        
        string = str(list(map(float, k)))[1:-1] + ',' + (str(DOI_list[k]))[1:-1] + '\n'
        fout.write(string)
    
    fout.close()

def main():

    csvs = input("Please provide 2 csv files (Separated by comma ','): \n")
    csv = csvs.split(',')
    res1= read_csv(csv[0])
    res2= read_csv(csv[1])
    print ('res1 is %s'% (csv[0]))
    print ('res2 is %s'% (csv[1]))
    DOI_list = full_list(res1, res2)
    write_file(DOI_list)

if __name__ == '__main__':
    main()

