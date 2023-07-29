# Python计算坐标集的中心点坐标


https://stackoverflow.com/a/68503006

```python
def get_centroid(points):
 
    x = points[:,0]
    y = points[:,1]
    
    # Solving for polygon signed area
    A = 0
    for i, value in enumerate(x):
        if i + 1 == len(x):
            A += (x[i]*y[0] - x[0]*y[i])
        else:
            A += (x[i]*y[i+1] - x[i+1]*y[i])
    A = A/2
 
    #solving x of centroid
    Cx = 0
    for i, value in enumerate(x):
        if i + 1 == len(x):
            Cx += (x[i]+x[0]) * ( (x[i]*y[0]) - (x[0]*y[i]) )
        else:
            Cx += (x[i]+x[i+1]) * ( (x[i]*y[i+1]) - (x[i+1]*y[i]) )
    Cx = Cx/(6*A)
 
    #solving y of centroid
    Cy = 0
    for i , value in enumerate(y):
        if i+1 == len(x):
            Cy += (y[i]+y[0]) * ( (x[i]*y[0]) - (x[0]*y[i]) )
        else:
            Cy += (y[i]+y[i+1]) * ( (x[i]*y[i+1]) - (x[i+1]*y[i]) )
    Cy = Cy/(6*A)
 
    return Cx, Cy
 
import numpy as np
points = np.array([[0, 0], [0, 1.1], [1, 0], [1, 1]])
```
