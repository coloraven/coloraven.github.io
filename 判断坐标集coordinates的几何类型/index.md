# 判断坐标集coordinates的几何类型


```python
import json

import geojson
from shapely.geometry import shape


def determine_geometry(coords: list):
    # 改装自https://stackoverflow.com/a/73100925
    if not coords:
        return "invalid geometry"
    if isinstance(coords[0], (int, float)):
        return "Point" if len(coords) >= 2 else "incomplete/invalid"
    elif isinstance(coords[0], list):
        # line, polygon or other
        if len(coords) >= 2 and isinstance(coords[0][0], (int, float)):
            # LineString or MultiPoint
            return "LineString"
        elif isinstance(coords[0][0], list):
            if isinstance(coords[0][0][0], (int, float)):
                return "Polygon" if len(coords) > 1 else "Polygon" # Polygon 
            else:
                # probably MultiPolygon
                return "MultiPolygon"



def to_wkt(coordinates: list):
    type_ = determine_geometry(coordinates)
    GeoJson = {"coordinates": coordinates, "type": type_}
    s = json.dumps(GeoJson)
    try:
        g1 = geojson.loads(s)
    except:
        pass
    return shape(g1).wkt
```
