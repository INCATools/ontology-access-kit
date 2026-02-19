
#from src.oaklib import converters

from curies import Converter

id = "BFO:0000004"
converter = Converter()
x = converter.parse_uri(id)

print(x)