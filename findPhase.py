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
        phases = findPhase('../../VanderbiltCampus/Vanderbilt.net.xml', tl)
        ret += '{'
        for phase in phases:
            ret += '"' + phase + '"' + ', '
        ret = ret[:-2] + '}},\n'
    ret = ret[:-2] + '\n}'
    return ret

if __name__ == '__main__':
    tlList = ['202407913', '1443088096', '202514078', '3010263944', '1443088101']
    print createCXXMap(tlList)
