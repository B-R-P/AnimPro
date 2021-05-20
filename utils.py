from math import *
rotatez = lambda angle:(
        (cos(angle),-sin(angle),0),
        (sin(angle), cos(angle),0),
        (     0    ,0,     1     )
    )
rotatey = lambda angle:(
        (cos(angle) ,0,-sin(angle)),
        (    0      ,1,    0     ),
        (-sin(angle),0,cos(angle))
    )
rotatex = lambda angle:(
        (1,0,0),
        (0,cos(angle),-sin(angle)),
        (0,sin(angle),cos(angle))
    )

def matmul(X,Y):
    result = []
    for i in range(len(X)):  
        ls=[]
        for j in range(len(Y[0])):  
            out=0
            for k in range(len(Y)):
                out += X[i][k] * Y[k][j]
            ls.append(out)
        result.append(ls)
    return tuple(tuple(i) for i in result)
def into2d(point):
    if len(point)==2:
        return point
    return list(point)[:-1]
def rotatedpoint(angle,point):
    return matmul(rotatey(angle),((i,)for i in point))
def percentopxs(pos,max_h,max_w):
        #        X-axis           Y-axis
    return max_h*pos[0]/100,max_w*pos[1]/100
def percentopx(v,mx):
    return mx*v/100
# Distance Formula[sqrt((x2-x1)^2 + (y2-y1)^2)]
dform = lambda p1,p2:((p2[0]-p1[0])**2+(p2[1]-p1[1])**2)**(1/2)
def increase(p1,p2,size):
    d = dform(p1,p2)
    bx,by = p2
    bx +=((bx- p1[0])/d)* size;
    by +=((by- p1[1])/d)* size;
    return bx,by
style2dict = lambda style:\
            {
            part[0].strip():part[1]
            for part in [
                    part.split(":") 
                    for part in style.split(";")
                    if part.strip()
                    ]
            }
dict2style = lambda dic:\
        ";".join(
                map(
                        lambda c:'{0}:{1}'.format(c[0],c[1]),
                        dic.items()
                    )
                )+';'
def centerer(center,ls):
    x,y = center
    l1,l2 =ls
    l1/=2
    l2/=2
    return (x-l1,y-l2),(x+l1,y+l2)
from itertools import zip_longest as zip
def combineGen(gens):
    for gen in zip(*gens):
        d1=gen[0].attribs
        style={}
        if 'style' in d1:
            style.update(style2dict(d1['style']))
        for d2 in gen[1:]:
            if d2:#Not None
                n_attribs=d2.attribs 
                if 'style' in n_attribs:
                    style.update(style2dict(n_attribs.pop('style')))
                d1.update(n_attribs)
        d1['style']=dict2style(style)
        yield gen[0]