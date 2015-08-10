import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json

file_in = 'reduced_columbus.osm'

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
		address = {}
		addresspart = re.compile(r'^addr:([a-z]|_)*$')
		street_part = re.compile(r'^addr:([a-z]|_)*:([a-z]|_)*$')		
		for tag in element.iter('tag'):
			if re.search(addresspart,tag.attrib['k']): #Assign Address
				address[tag.attrib['k'][5:]]=tag.attrib['v']
		node['address']=address
		return node
	else:
		return None		



def process_map(file_in,pretty=False):
    file_out = "{0}.json".format('reduced_columbus')
    data = []
    with codecs.open(file_out, "w") as fo:
    		for _, element in ET.iterparse(file_in):
    			el = shape_element(element)
    			if el:
    				print el
    				data.append(el)
    				if pretty:
    					fo.write(json.dumps(el,indent=2)+'\n')
    				else:
    					fo.write(json.dumps(el)+'\n')
    return data						

            
process_map(file_in)   