import matplotlib.pyplot as plt
import numpy as np



measurements = {'InterstripR': [],
                'Pinhole': [],
                'InterstripC': [],
                }


def calculateResistance(v, i):
    fit = np.polyfit(i, v, 1)
    print fit[0]
    return fit[0]

def getMeasurementsResults(lines, measurementType, start, data, iStrip):
    result = 0.0
    if measurementType == 'InterstripR':
        v = []
        i = []
        while len(lines[start].split()) == 2:
            if float(lines[start].split()[0]) != 0:
                v.append(float(lines[start].split()[0]))
                i.append(float(lines[start].split()[1]))
            start += 1
        result = calculateResistance(v, i)
    elif measurementType == 'Pinhole':
        result = 10.0/float(lines[start].split()[1])
    elif measurementType == 'InterstripC':
        result = float(lines[start].split()[2])


    data.append((iStrip, result))
    return start


def getMeasurementType(line, nextLine):
    if 'Interstrip R' in line:
        return 'InterstripR'
    elif 'Bias V' in line:
        if 'Pinhole' in nextLine:
            return 'Pinhole'
        elif 'Interstrip C' in nextLine:
            return 'InterstripC'
    else:
        print 'type %s not supported' %line
        return 'null'

def getTitle(measurementType):
    if measurementType == 'InterstripR':
        return 'Interstrip Resistance Measurement'
    elif measurementType == 'InterstripC':
        return 'Interstrip Capacitance Measurement'
    elif measurementType == 'Pinhole':
        return 'Pinhole Measurement'

def getYAxis(measurementType):
    if measurementType == 'InterstripR':
        return r'Interstrip Resistance ($\Omega$)'
    elif measurementType == 'InterstripC':
        return 'Interstrip Capacitance (F)'
    elif measurementType == 'Pinhole':
        return r'Resistance ($\Omega$)'


def plotter(measurementType, data, i):
    strips = []
    results = []

    plt.figure(i)
    for i in range(len(data)):
        strips.append(data[i][0])
        results.append(data[i][1])
    plt.semilogy(strips, results, 'ro')
    if measurementType == 'InterstripR':
        results = [1,2,3]
    print measurementType
    print strips
    print results
    plt.xticks(np.arange(min(strips), max(strips)+1, 1.0))

    plt.suptitle(getTitle(measurementType))
    plt.xlabel('strips')
    plt.ylabel(getYAxis(measurementType))
    plt.savefig('%s.pdf' %measurementType)
    

def read(fileLocation):
    f = open(fileLocation, "r").readlines()
    i = 0
    while i < len(f):
        currentLine = f[i]

        if 'Strip' in currentLine:
            iStrip = int(currentLine.split()[1])
            measurementType = getMeasurementType(f[i+1], f[i+2])
            nextLine = getMeasurementsResults(f, measurementType, i+2, measurements[measurementType], iStrip)
            i = nextLine
        i+= 1
    i = 0
    for iMeasType in measurements.keys():
        plotter(iMeasType, measurements[iMeasType], i)
        i+=1

read('Test7.txt')