""" plot the 2x2 residue between two conditions (e.g. different views)
current version works for RPI-DD inspections, plane0=R, plane1=T
use full sigma as x
use other sigma as y
"""

from glob import glob
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt

def read_ir(ir):
    """ read one residue.txt, get all the coordinates, and and residues from different planes,
    sort it and output a sorted list of tuples
    input: residue.txt from 'Review -saveResidueStats'
    intermediate output: [((x,y),(plane0 residue, plane1 residue)), ...]
    final output: [(plane0 residue, plane1 residue)), ...] after sorting (x,y)
    """

    residue = []
    with open(ir, 'r') as fin:
        for line in fin:
            if line not in ('\n', '\r\n') and line.split()[0].isdigit():
                x = line.split()[1]
                y = line.split()[2]
                R = int(line.split()[3])
                T = int(line.split()[4])

                residue.append(((x,y),(R,T)))
    # sort by x,
    DOI = sorted(residue, key=lambda x: x[0][0])
    # then sort by y
    DOI = sorted(DOI, key=lambda y: y[0][1])

    #choose point defects only based on location
    RRes = [res[1][0] for res in DOI][0:361]
    TRes = [res[1][1] for res in DOI][0:361]

    return (RRes, TRes)

def ave_ir(irs):
    '''calculate the average residue, and std from several repeats'''

    RTotal = []
    TTotal = []
    for ir in irs:
        RTotal.append(read_ir(ir)[0])
        TTotal.append(read_ir(ir)[1])

    Rarr = np.asarray(RTotal)
    Rave = np.mean(Rarr, axis=0)
    Rstd = np.std(Rarr, axis=0)

    Tarr = np.asarray(TTotal)
    Tave = np.mean(Tarr, axis=0)
    Tstd = np.std(Tarr, axis=0)

    return Rave, Tave, Rstd, Tstd

def filterDef(x1, xstd1, y1, ystd1):
    '''remove defects with residue > certain gs, and maintain the order of x,y, return np arrays
    input: numpy arrays
    output: numpy array [x, xstd, y, ystd]
    '''

    arr = np.asarray([x1, xstd1, y1, ystd1])
    filtering = arr[:, arr[2] < 80] # keep defects with residue < 80gs
    return (filtering)

def fitting(Rx, Rxstd, Ry, Rystd, Tx, Txstd, Ty, Tystd, xname, yname):
    '''plot residues and linear fit'''

    plt.subplot(1, 2, 1)
    slope, intercept, r_value, p_value, slope_std_error = stats.linregress(Rx, Ry)
    line = slope * Rx + intercept
    #plt.plot(Rx, Ry, 'o', label="residue")
    plt.errorbar(Rx, Ry, xerr=Rxstd, yerr=Rystd, fmt='o', label="residue")
    plt.plot(Rx, line, color="red", linewidth=1.0, linestyle="-", label="linear fit")
    plt.plot(Rx, 1.0*Rx, color="green", linewidth=1.0, linestyle=":", label="45 degree")
    plt.title(r"Reflected", fontsize="20")
    plt.xlabel("%s"% xname, fontsize="18")
    plt.ylabel("%s"% yname, fontsize="18")
    plt.legend(loc='upper left')
    plt.text(60, 45, 'slope=%s\n'% round(slope,3) +\
               'intercept=%s\n'% round(intercept,2) +\
             'r-square=%s'% round(r_value**2, 2), fontsize=16, color='b')

    plt.subplot(1, 2, 2)
    slope, intercept, r_value, p_value, slope_std_error = stats.linregress(Tx, Ty)
    line = slope * Tx + intercept
    #plt.plot(Tx, Ty, 'o', label="residue")
    plt.errorbar(Tx, Ty, xerr=Txstd, yerr=Tystd, fmt='o', label="residue")
    plt.plot(Tx, line, color="red", linewidth=1.0, linestyle="-", label="linear fit")
    plt.plot(Tx, 1.0*Tx, color="green", linewidth=1.0, linestyle=":", label="45 degree")
    plt.title(r"Transmitted", fontsize="20")
    plt.xlabel("%s"% xname, fontsize="18")
    plt.ylabel("%s"% yname, fontsize="18")
    plt.legend(loc='upper left')
    plt.text(50, 30, 'slope=%s\n'% round(slope,3) +\
               'intercept=%s\n'% round(intercept,2) + \
             'r-square=%s' % round(r_value ** 2, 2), fontsize=16, color='b')

    #plt.savefig("test.png")
    plt.show()

def bar(Rx, Ry, Tx, Ty, xname, yname):
    '''plot normalized residue diff （%）'''

    plt.subplot(1, 2, 1)
    diff_R = 100*(Ry - Rx)/Rx
    aveDiff_R = round(float(np.average(diff_R)), 2)
    stdDiff_R = round(float(np.std(diff_R)), 2)
    print('stdDiff_R= %s'%stdDiff_R )
    ind_R = np.arange(len(diff_R))
    # calculate std
    std_low_R = aveDiff_R + stdDiff_R + 0*diff_R
    std_high_R = aveDiff_R - stdDiff_R + 0*diff_R
    width = 0.35

    plt.bar(ind_R, diff_R, width = width, color ='b', edgecolor = 'b', label="(%s-%s)/%s (%%)"%(yname, xname, xname))
    # plot a constant line with the average value
    plt.plot(ind_R, aveDiff_R+0*diff_R, color="red", linewidth=3.0, linestyle=":", label="average: %s%%"% aveDiff_R)
    # plot 1 sigma std
    plt.fill_between(ind_R, std_low_R, std_high_R, color = 'green', alpha = '0.75')
    plt.title(r"Reflected", fontsize="20")
    plt.xlabel("%s"% xname, fontsize="18")
    plt.ylabel("%s"% yname, fontsize="18")
    plt.legend(loc='upper left')

    plt.subplot(1, 2, 2)
    diff_T = 100*(Ty - Tx)/Tx
    aveDiff_T = round(float(np.average(diff_T)), 2)
    stdDiff_T = round(float(np.std(diff_T)), 2)
    print('stdDiff_T= %s' % stdDiff_T)
    ind_T = np.arange(len(diff_T))
    std_low_T = aveDiff_T + stdDiff_T + 0 * diff_T
    std_high_T = aveDiff_T - stdDiff_T + 0 * diff_T
    width = 0.35

    plt.bar(ind_T, diff_T, width = width, color ='b', edgecolor = 'b', label="(%s-%s)/%s (%%)"%(yname, xname, xname))
    plt.plot(ind_T, aveDiff_T+0*diff_T, color="red", linewidth=3.0, linestyle=":", label="average: %s%%"% aveDiff_T)
    plt.fill_between(ind_T, std_low_T, std_high_T, color='green', alpha='0.75')
    plt.title(r"Transmitted", fontsize="20")
    plt.xlabel("%s"% xname, fontsize="18")
    plt.ylabel("%s"% yname, fontsize="18")
    plt.legend(loc='upper left')

    plt.show()

if __name__ == '__main__':
    irsx = glob(input('IRs (X axis)> '))
    Rx1, Tx1, Rx1std, Tx1std = ave_ir(irsx)
    irsy = glob(input('IRs (Y axis)> '))
    Ry1, Ty1, Ry1std, Ty1std = ave_ir(irsy)

    xname = input('X axis name> ')
    yname = input('Y axis name> ')

    Rx,  Rxstd, Ry, Rystd = filterDef(Rx1, Rx1std, Ry1, Ry1std)
    Tx,  Txstd, Ty, Tystd = filterDef(Tx1, Tx1std, Ty1, Ty1std)

    fitting(Rx, Rxstd, Ry, Rystd, Tx, Txstd, Ty, Tystd, xname, yname)
    bar(Rx, Ry, Tx, Ty, xname, yname)

    # R170422.R170422-PDM2015-SN6001-55RT-DD-N15-LS-3x-fullsigma*
    # R170422.R170422-PDM2015-SN6001-55RT04-DD-N15-LS-3x-half*


