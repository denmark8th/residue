'''
*select defects with averaged (through-focus) defect signal between 15gs and 60gs.
*for defect n at focus offset f
Val(n, f) = 1 if the defect signal is the largest among all focus offsets for defect n
Val(n, f) = 0 if the defect signal is not the largest among all focus offsets for defect n
*sum up Val of all defects for each FO
*pick the best focus offset with largest sum of Val
'''


def read(file, minRes, maxRes):
    '''
    '''
    with open(file, 'r') as fin:

        count ={}
        for line in fin:
            if 'defect' in line:
                FO = line.split(',')[5:]

            if ('residue' not in line) and ('defect' not in line):
                residue = line.split(',')[5:]
                #convert str residue to int residue
                IntRes = list(map(lambda x: int(x), residue))
                ave = sum(IntRes)*1.0/len(IntRes)

                
                if minRes < ave < maxRes:
                    #find the index of the max residue for this defect
                    pos = residue.index(max(residue))
                    posFocus = FO[pos]
                    

                    count[posFocus] = count.get(posFocus,0) +1

    for key in count.keys():
        print (('FO=%s, count=%s')%(key, count[key]))
    print (('total count = %s')%(sum(count.values())))
            
def main():
    file = input('> ')
   # minRes = float(input('lowest residue to calculate: '))
  #  maxRes = float(input('hightest residue to calculate: '))
    minRes = 15
    maxRes = 70
    read(file, minRes, maxRes)

if __name__=='__main__':
    main()
