#ITERATIVE PARSING EXAMPLE
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
from sys import argv

script, file_in = argv
osm_file = open(file_in,'r')


street_type_re = re.compile(r'\S+\.?$', re.IGNORECASE)
street_types = defaultdict(int)
# \S: A sequence of 
# +: non whitespace characters.
# \.?: Optionally followed by a period.
# $ This match must occur at the end of the string.

def audit_street_type(street_types,street_name):
	m = street_type_re.search(street_name)
	if m:
		street_type = m.group()
		street_types[street_type] += 1	

def print_sorted_dict(d):
	keys = d.keys()
	keys = sorted(keys, key = lambda s:s.lower())
	for k in keys:
		v = d[k]
		print '%s: %d' % (k,v)

def is_street_name(elem):
	return (elem.tag == 'tag') and (elem.attrib['k'] == 'addr_street')


def audit():
	for _, element in ET.iterparse(osm_file):
		if element.tag == "node" or element.tag == "way":
			for tag in element.iter('tag'):	
				audit_street_type(street_types,tag.attrib['v'])
	print_sorted_dict(street_types)
	
audit()						
