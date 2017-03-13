import os
import ast
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


class Submap(object):
    def __init__(self, name, edges):
        self.name = name
        self.edges = edges

    @staticmethod
    def generate_submaps(jfile):
        f = open(jfile, 'r')
        st = f.read()
        lst = ast.literal_eval(st)
        ret = []
        for ele in lst:
            name = ele['color']
            edges = ele['edges']
            tmp = Submap(name, edges)
            ret.append(tmp)
        return ret

    def in_this_map(self, edge):
        return edge in self.edges


def get_matric(maps, dumpfile):
    distance = {}
    time = {}
    for m in maps:
        distance[m.name] = 0
        time[m.name] = 0
#    distance['other'] = 0
 #   time['other'] = 0

    xmlfile = open(dumpfile, 'r')
    #xmlTree = ET.parse(xmlfile)
    xmlTree = ET.iterparse(xmlfile,events=("start", "end"))
   # treeRoot = xmlTree.getroot()
   # stepNumber = len(treeRoot)


    map_id = None
    for event, node in xmlTree:
        if event == 'start' and node.tag == 'edge':
            for m in maps:
                if m.in_this_map(node.attrib['id']):
                    map_id = m.name
                    break
        elif event == 'start' and node.tag == 'vehicle':
            assert not map_id == None
            speed = float(node.attrib['speed'])
            time[map_id] += 1
            distance[map_id] += speed

        elif event == 'end' and node.tag == 'edge':
            map_id = None

        node.clear()


    xmlfile.close()
    g_distance = 0
    g_time = 0
    for k in distance.keys():
        g_distance += distance[k]
        g_time += time[k]
        distance[k] = distance[k]/time[k]
    return distance, g_distance/g_time

if __name__ == '__main__':
    maps = Submap.generate_submaps(os.path.join('submap','map.regions3.json'))
    import sys
    distance, avg = get_matric(maps, sys.argv[1])
    print distance, avg
