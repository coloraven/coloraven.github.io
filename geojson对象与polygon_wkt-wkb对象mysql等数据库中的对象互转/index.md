# geojson对象与polygon_wkt、wkb对象（MySQL等数据库中的对象）互转


来源：https://gist.github.com/drmalex07/5a54fc4f1db06a66679e

```python
import json
import geojson
from shapely.geometry import shape
 
o = {
   "coordinates": [[[23.314208, 37.768469], [24.039306, 37.768469], [24.039306, 38.214372], [23.314208, 38.214372], [23.314208, 37.768469]]], 
   "type": "Polygon"
}
 
s = json.dumps(o)
 
# Convert to geojson.geometry.Polygon
g1 = geojson.loads(s)
 
# Feed to shape() to convert to shapely.geometry.polygon.Polygon
# This will invoke its __geo_interface__ (https://gist.github.com/sgillies/2217756)
g2 = shape(g1)
 
# Now it's very easy to get a WKT/WKB representation
g2.wkt
g2.wkb
import geojson
import shapely.wkt
 
s = '''POLYGON ((23.314208 37.768469, 24.039306 37.768469, 24.039306 38.214372, 23.314208 38.214372, 23.314208 37.768469))'''
 
# Convert to a shapely.geometry.polygon.Polygon object
g1 = shapely.wkt.loads(s)
 
g2 = geojson.Feature(geometry=g1, properties={})
 
g2.geometry
```


