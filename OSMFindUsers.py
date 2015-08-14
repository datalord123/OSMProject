#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
from sys import argv

script, osm_file = argv
def get_user(element):
    return

def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        if element.tag== 'node':
            uid= element.get('uid')
            users.add(uid)

    return users


def test():

    users = process_map(osm_file)
    print len(users)



if __name__ == "__main__":
    test()