'''
'''

import xml.etree.ElementTree as ET
from glob import glob

def data(xml_list):
    res = dict()

    for xml in xml_list:

        tree = ET.parse(xml)
        root = tree.getroot()

        for child in root[0][0]:
            x = int(child.attrib['X'][:5])/100
            y = int(child.attrib['Y'][:4])/100
            name = xml.split(".")[0]
            id = child.attrib['Index']
            patchY = child.attrib['PatchOffsetY']

            res[(x,y)] = res.get((x,y), []) + [name, id, patchY]
    return (res)

def write(res):
    with open('fd.csv', 'w') as fout:
        fout.write('X'+','+'Y'+',')

        irs = list(res.values())[0]
        i = 0
        while i < len(irs):
            fout.write('ir'+','+'id'+','+'patchY'+',')
            i += 3
        fout.write('\n')

        for key in res:
            fout.write(str(key[0])+','+str(key[1])+',')
            for item in res[key]:
                fout.write(str(item) + ',')
            fout.write('\n')

if __name__ == '__main__':
    xml_list = glob('*xml')
    res = data(xml_list)
    write(res)