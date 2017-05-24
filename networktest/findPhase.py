import sys

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


def findPhase(campusMapNet, controller):
    xmlfile = open(campusMapNet, 'r')
    xmlTree = ET.parse(xmlfile)
    treeRoot = xmlTree.getroot()
    ret = []
    for child in treeRoot:
        if child.tag != 'tlLogic':
            continue
        if child.attrib['id'] != controller:
            continue

        for phase in child:
           ret.append(phase.attrib['state'])
        break
    xmlfile.close()
    return ret


def createCXXMap(tlList):
    ret = '{\n'
    for tl in tlList:
        ret += '{' + '"Controller' + tl + '"'
        phases = findPhase('sumo/grid.net.xml', tl)
        ret += '{'
        for phase in phases:
            ret += '"' + phase + '"' + ', '
        ret = ret[:-2] + '}},\n'
    ret = ret[:-2] + '\n}'
    return ret

if __name__ == '__main__':
    tlList = ['1/2', '2/2', '1/1', '2/1']
    print createCXXMap(tlList)
