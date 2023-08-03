# 判断点是否在多边形内（check is the point in polygon）


## 方法一（参考[Python一行代码处理地理围栏](https://www.icode9.com/content-1-92489.html)）

```python
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
 
polygon_data= [[114.3458104133606,30.476167529462785],[114.34512376785278,30.475575748963195],[114.34576749801636,30.474540124433936],[114.3467652797699,30.475363076967565],[114.34693694114685,30.476102803645833],[114.3458104133606,30.476167529462785]]
          
point1 = Point([114.34605717658997,30.475584995561178])
point2 = Point([114.346604347229,30.476518897432545])
polygon = Polygon(polygon_data)
print(polygon.contains(point1))
print(polygon.contains(point2))
#输出
# True
# False
```

## 方法二 光线追踪

```python
def is_inside_sm(polygon, point):
    length = len(polygon)-1
    dy2 = point[1] - polygon[0][1]
    intersections = 0
    ii = 0
    jj = 1
    while ii<length:
        dy  = dy2
        dy2 = point[1] - polygon[jj][1]
        # consider only lines which are not completely above/bellow/right from the point
        if dy*dy2 <= 0.0 and (point[0] >= polygon[ii][0] or point[0] >= polygon[jj][0]):
 
            # non-horizontal line
            if dy<0 or dy2<0:
                F = dy*(polygon[jj][0] - polygon[ii][0])/(dy-dy2) + polygon[ii][0]
                if point[0] > F: # if line is left from the point - the ray moving towards left, will intersect it
                    intersections += 1
                elif point[0] == F: # point on line
                    return 2
            # point on upper peak (dy2=dx2=0) or horizontal line (dy=dy2=0 and dx*dx2<=0)
            elif dy2==0 and (point[0]==polygon[jj][0] or (dy==0 and (point[0]-polygon[ii][0])*(point[0]-polygon[jj][0])<=0)):
                return 2
        ii = jj
        jj += 1
    #print 'intersections =', intersections
    return intersections & 1  
 
polygon_data= [[114.3458104133606,30.476167529462785],[114.34512376785278,30.475575748963195],[114.34576749801636,30.474540124433936],[114.3467652797699,30.475363076967565],[114.34693694114685,30.476102803645833],[114.3458104133606,30.476167529462785]]
points = [[114.34605717658997,30.475584995561178],[114.346604347229,30.476518897432545]]
for point in points:
    x = is_inside_sm(polygon_data,point)
    print(x)
```

## 方法三

[参考一：Python一行代码处理地理围栏](https://stackoverflow.com/a/66189882)
[参考二：Python中检查点是否在多边形内，哪种方法是最快的](https://stackoverflow.com/a/66189882)

[参考二中提到的最快算法来源 Github源码](https://github.com/sasamil/PointInPolygon_Py)
