import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
from sys import argv


script, file_in, file_out = argv

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

def shape_element(element):
	node = {}
	pos=[]
	if element.tag == "node" or element.tag == "way":
		if 'id' in element.attrib:
			node['id'] = element.attrib['id']
		node['type'] = element.tag
		if 'visible' in element.attrib:
			node['visible'] = element.attrib['visible']
		created = {}
		for i in CREATED:
			created[i]=element.attrib[i]
		node['created']=created
		if 'lat' in element.attrib:
			pos.append(float(element.attrib['lat']))
        if 'lon' in element.attrib:  
        	pos.append(float(element.attrib['lon']))		
		node['pos']=pos
		addresspart = re.compile(r'^addr:([a-z]|_)*$')
		street_part = re.compile(r'^addr:([a-z]|_)*:([a-z]|_)*$')		
		address = {}
		for tag in element.iter('tag'):
			if re.search('addr:',tag.attrib['k']):
				address[tag.attrib['k'][5:]]=tag.attrib['v']
			#if re.search(addresspart,tag.attrib['k']): #Assign Address
			#	address[tag.attrib['k'][5:]]=tag.attrib['v']
				#print tag.attrib['k'],tag.attrib['v']
		print address
		#node['address']=address
		return node
	else:
		return None		

def process_map(file_in,file_out,pretty=False):
    file_out = "{0}.json".format(file_out)
    data = []
    with codecs.open(file_out, "w") as fo:
    		for _, element in ET.iterparse(file_in):
    			el = shape_element(element)
    			#if el:
    			#	print el
    			#	data.append(el)
    			#	if pretty:
    			#		fo.write(json.dumps(el,indent=2)+'\n')
    			#	else:
    			#		fo.write(json.dumps(el)+'\n')
    return data						

            
process_map(file_in,file_out)   