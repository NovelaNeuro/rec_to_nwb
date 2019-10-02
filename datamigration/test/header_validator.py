import xmlschema
from xml.etree import ElementTree
import json

xs = xmlschema.XMLSchema('/Users/bigblue/Novela/fl_lab_header.xsd')
xt = ElementTree.parse('/Users/bigblue/Novela/fl_lab_header.xml')
root = xt.getroot()

#validation against xsd schema
print(xs.is_valid(xt))

print( len(root[1][0]))

for child in root[1][0]:
    print(child.tag, child.attrib)

for child in root:

# if not tag:
# for c in tag:
# print("Inside: ", c.tag, c.attrib)
    print("Main tag: ", child.tag, child.attrib)