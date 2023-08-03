# Python中sqlite使用spatial扩展


```python
import sqlite3
 
connR = sqlite3.connect(':memory:')
 
connR.enable_load_extension(True)
 
#now we can load the extension
# depending on your OS and sqlite/spatialite version you might need to add 
# '.so' (Linux) or '.dll' (Windows) to the extension name
 
#mod_spatialite (recommended)
connR.execute('SELECT load_extension("mod_spatialite")')   
connR.execute('SELECT InitSpatialMetaData(1);')  
 
# libspatialite
connR.execute('SELECT load_extension("libspatialite")')
connR.execute('SELECT InitSpatialMetaData();')
 
curR = connR.cursor()
 
 
curR.execute('''CREATE TABLE my_line(id INTEGER PRIMARY KEY)''')
curR.execute('SELECT AddGeometryColumn("my_line","geom" , 4326, "LINESTRING", 2)')
connR.commit()
 
polygon_wkt = 'POLYGON ((11 50,11 51,12 51,12 50,11 50))'
 
XA = 11
YA = 52
XB = 12
YB = 49
 
line_wkt = 'LINESTRING({0} {1}, {2} {3})'.format(XA, YA, XB, YB)
 
curR.execute("""INSERT INTO my_line VALUES (?,GeomFromText(?, 4326))""", (1, line_wkt))
 
connR.commit()
 
cursor = connR.execute('''
    SELECT astext(st_intersection(geom, GeomFromText(?, 4326))) from my_line
    WHERE st_intersects(geom, GeomFromText(?, 4326))''', (polygon_wkt, polygon_wkt))
 
for item in cursor:
    print(item)
```

[python sqlite使用spatial扩展](https://gis.stackexchange.com/a/244830)
