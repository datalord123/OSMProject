Traceback (most recent call last):
    File "OSMProjectProcess.py", line 93, in <module>
    process_map(file_in,file_out)
        File "OSMProjectProcess.py", line 75, in process_map
if el['address']['street']:
KeyError: 'street'import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
from sys import argv


script, file_in, file_out = argv

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

mapping = { "St": "Street",
            "St.": "Street",
            'Rd': 'Road',
            'Rd.': 'Road',
            'Ave': 'Avenue',
            'Ave.': 'Avenue',
            'Ln':'Lane',
            'Ln.':'Lane',
            'Dr':'Drive',
            'Dr.':'Drive',
            'Pl':'Place',
            'Pl.':'Place',
            'Pkwy':'Parkway'
            }

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
           	#elif re.search(problemchars,tag.attrib['k']): 
            #	break                        
           	#elif re.search(street_part, tag.attrib['k']): 
            #   	break
           	#elif re.search(lower_colon, tag.attrib['k']):
            #    node[tag.attrib['k']] = tag.attrib['v']   
		node['address']=address
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
    			#	if el['address']['street']:
    			#		pass
    					#$print el['address']['street']
    			#		print el['address']
    				#['street']
    				#if len(el['address']) != 0: #Fix Street name here
    				#	print el
    					#for k,v in el['address'].iteritems():
    					#	if k == 'street':
    					#		print k,v
    				#	print el
    			#	data.append(el)
    			#	if pretty:
    			#		fo.write(json.dumps(el,indent=2)+'\n')
    			#	else:
    			#		fo.write(json.dumps(el)+'\n')
    return data						

            
process_map(file_in,file_out)   

'''
                
'''
'''
def update_name(name, mapping):
    for key,value in mapping.iteritems():
        if key in name:
            name = re.sub(street_type_re,value,name)
    return name
'''    