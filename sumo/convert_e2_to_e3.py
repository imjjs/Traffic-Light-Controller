try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

import re


# NS_GREEN, WE_GREEN, w, e, n, s
# WE_RED, NS_Red
IN_DATA = {
    "1443088101": ["GGGggrrrrGGGggrrrr", "rrrrrGGggrrrrrGGgg", 3, 2, 2, 2],#
    "202270699": ["GGGGgrrrGGGggrrr", "rrrrrGGgrrrrrGgg", 1, 2, 3, 3],
    "202514063": ["GGGGggrrrrGGGGggrrrr", "rrrrrrGGggrrrrrrGGgg", 2, 1, 3, 3],#
    "202305800": ["GGGGggrrrrGGGGggrrrr", "rrrrrrGGggrrrrrrGGgg", 1, 1, 3, 3],#
    "202514074": ["GGGrrrrGgGrrrr", "rrGGGGgrrGGGGg", 3, 3, 2, 2],#
    "202514078": ["GGGGggrrrrGGGGggrrrr", "rrrrrrGGggrrrrrrGGgg", 1, 2, 3, 3],#
    "3010263944": ["GGggrrrrrGGggrrrrr", "rrrrGGGggrrrrGGGgg", 2, 2, 2, 2],#
    "1443088096": ["GGGGggrrGGGGggrrrr", "GrrrrrGGrrrrrrGGgg", 1, 2, 3, 3],#
    "202407913": ["GGGggGGGGgrrrr", "rrrrrrrrrrGGGG", 0, 2, 3, 3],#
    "IK" :["Grr", "rGG", 2, 0, 1, 0],
    "LJ" :["Grr", "rGG", 2, 0, 1, 0],
    "GD" :["Grr", "rGG", 2, 0, 1, 0],
    "FH" :["Grr", "rGG", 2, 0, 1, 0],
    "AC" :["GGrr", "rrGG", 2, 0, 2, 0],
}



pattern = '{junction_name}S{direction}{idx}'




def findJunction(junc_name, input):
    inf = []
    ret = ''
    for e2 in input.iter('e2Detector'):
        rex = pattern.format(junction_name = junc_name, direction = '.', idx = '\d')
        crex = re.compile(rex)
        if crex.match(e2.get('id')):
            inf.append(e2)
    if 0 == len(inf):
        return ''


    #north
    ret += setDirection(junc_name, 'N', inf)
    ret += setDirection(junc_name, 'S', inf)
    ret += setDirection(junc_name, 'E', inf)
    ret += setDirection(junc_name, 'W', inf)
    return ret

def setDirection(junc_name ,direction_name, inf):
    junction_p = re.compile(pattern.format(junction_name = junc_name, direction = direction_name, idx ='\d'))
    ele_list = []
    for ele in inf:
        if junction_p.match(ele.get('id')):
            ele_list.append(ele)
    if len(ele_list) == 0:
        return ''

    et_name = junc_name + direction_name
    #north
    direct = ET.Element('entryExitDetector')
    direct.set('id', et_name)
    direct.set('freq', '1')
    direct.set('file', 'NUL')
    for ele in ele_list:
        entry = ET.SubElement(direct, 'detEntry')
        exit = ET.SubElement(direct, 'detExit')
        entry.set('lane', ele.get('lane'))
        exit.set('lane', ele.get('lane'))
        entry.set('pos', ele.get('pos'))
        exit.set('pos', str(float(ele.get('pos')) + float(ele.get('length'))))
        entry.set('friendlyPos', 'true')
        exit.set('friendlyPos', 'true')
    return ET.tostring(direct)


def main():

    xmlfile = open("detectors.xml", 'r')
    xmlTree = ET.parse(xmlfile)
    treeRoot = xmlTree.getroot()
    output = ''
    for k in IN_DATA.keys():
        output += findJunction(k,treeRoot)
    print output


    #for k,v in IN_DATA:


    # totalDuration = 0
    # carNumber = len(treeRoot)
    # for child in treeRoot:
    #     totalDuration += float(child.attrib['duration'])
    # res = totalDuration * 1.0 / carNumber
    #
    # xmlfile.close()
    # os.remove("tripinfo" + str(port) + ".xml")

if __name__ == '__main__':
    main()
