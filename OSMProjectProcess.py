import xml.etree.cElementTree as ET
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
            'Pkwy':'Parkway',
            'Blvd.': 'Boulevard',
            'Blvd': 'Boulevard'
            }

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons"]
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
		address_part = re.compile(r'^addr:(\w+|_)*$') #lower case only, fix to also include upper
		street_part = re.compile(r'^addr:(\w+)*:(\w+|_)*$') #lower case only, fix to also include upper
		
		for tag in element.iter('tag'):
			if re.search(problemchars,tag.attrib['k']): #Ignore keys that include problem Characters
				continue
			elif re.search(address_part,tag.attrib['k']): #if addr: in 'k' value then add to 'address' dictionary
				address[tag.attrib['k'][5:]]=tag.attrib['v']		
				#print tag.attrib['v']
			elif re.search(street_part,tag.attrib['k']): #ignore if addr: and second : exists
				continue
			else: #if k doesn't start with addr but contain : process like any other tag
				node[tag.attrib['k']]=tag.attrib['v']
		node['address']=address
		return node
	else:
		return None		

def update_name(name, mapping):
	for key,value in mapping.iteritems():
		if key in name:
			newname = re.sub(street_type_re,value,name)
			print name,'==>',newname
	return name

#Udacity Coach: here is a simple example: test = "Compton St 37"
#Udacity Coach: m = re.search('(.*)(key)(.*)', test, re.IGNORECASE)
#Udacity Coach: then, you can retrieve elements of the string using m.group(1)
#Udacity Coach: m.group(2)

def process_map(file_in,file_out,pretty=False):
    file_out = "{0}.json".format(file_out)
    data = []
    with codecs.open(file_out, "w") as fo:
    		for _, element in ET.iterparse(file_in):
    			el = shape_element(element)
    			if el:
    				if 'street' in el['address']:    					
    					old_street = el['address']['street']
    					new_street = update_name(old_street,mapping)
    					#print old_street, '==>', new_street
    					#$print el['address']['street']
    			#		print el['address']

    			#	data.append(el)
    			#	if pretty:
    			#		fo.write(json.dumps(el,indent=2)+'\n')
    			#	else:
    			#		fo.write(json.dumps(el)+'\n')
    return data						
            
process_map(file_in,file_out)   
 