import os

a = open("/exports/csce/datastore/geos/groups/MSCGIS/s2318635/240723/03sep19/gedisim/gedimetric_input.txt", "w")
for path, subdirs, files in os.walk(r'/exports/csce/datastore/geos/groups/MSCGIS/s2318635/240723/03sep19/gedisim/gedirat'):
   for filename in files:
     f = os.path.join(path, filename)
     a.write(str(f) + os.linesep) 


