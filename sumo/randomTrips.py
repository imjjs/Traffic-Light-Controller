#!/usr/bin/env python

from random import seed, random, sample
import xml.etree.ElementTree as ElementTree
import time

fromHome = [
  "19479801#0",
  "19470377#0",
  "120254976#0",
  "-19468772",
  "-245915229#14",
]

toHome = [
  "-19479801#0",
  "-19470377#0",
  "-120254976#0",
  "19468772",
  "-41139605#0",
]

seed(time.time())

tree = ElementTree.parse("Vanderbilt.net.xml")
root = tree.getroot()

edges = set()

for edge in root.iter('edge'):
  attributes = edge.attrib
  if attributes.get('function') != "internal":
    edges.add(attributes['id'])

def colorComponent():
  return str(random() * 0.5 + 0.5)

print "<trips>"
print '  <vType accel="1.0" decel="5.0" id="Car" length="3.0" maxSpeed="100.0" sigma="0.0" />'

periods = [
 { 'fromHome': 125, # morning
   'toHome': 25,
   'intra': 75,
   'length': 20,
 },
  #{ 'fromHome': 25, # midday
  #  'toHome': 25,
  #  'intra': 75,
  #  'length': 20,
#  },
#  { 'fromHome': 25, # afternoon
 #   'toHome': 125,
 #   'intra': 75,
#    'length': 20,
 # },  
 #  { 'fromHome': 25, # night
 #    'toHome': 25,
 #    'intra': 50,
 #    'length': 60,
 # },
]

flowID = 0

def addFlow(begin, end, source, destination):
  global flowID
  if (source != "-" + destination) and (destination != "-" + source):
    print '<flow id="flow' + str(flowID) + '" begin="' + str(begin) + '" probability="0.011" end="' + str(end) + '" type="Car" from="' + source + '" to="' + destination + '" color="' + colorComponent() + ',' + colorComponent() + ',' + colorComponent() + '"/>'
    flowID = flowID + 1

begin = 0

for period in periods:
  end = begin + period['length'] * 60
  
  for route in range(period['fromHome']):
    addFlow(begin, end, sample(fromHome, 1)[0], sample(edges, 1)[0])
    
  for route in range(period['toHome']):
    addFlow(begin, end, sample(edges, 1)[0], sample(toHome, 1)[0])
    
  for route in range(period['intra']):
    endPoints = sample(edges, 2)
    addFlow(begin, end, endPoints[0], endPoints[1])
    
  begin = end

print "</trips>"
  
  
  
  
