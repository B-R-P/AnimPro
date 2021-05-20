from utils import *
class BaseElement:
    def __init__(self,state,pos,style,screen):
        self.current_state =  state
        self.pos  = pos
        self.style=style2dict(style.replace(";;",";"))
        self.screen = screen
    def addAttribute(self,attribute,content):
        nattribute = ""
        attribs = self.current_state.attribs
        if atrribute in attribs:
            nattribute=attribs[attribute]+";"
        nattribute+=content
        self.current_state.attribs[attribute]=nattribute
    def changeAttribute(self,attribute,content):
        self.current_state.update({attribute:content})
    def rotate(self,angle):
        self.current_state.attribs['transform'] = \
            'rotate({0} {1} {2})'.format(angle,*self.center())
    def flip(self,angle):
        rotatex_angle = rotatez(angle)
        x1,y1=self.pos
        x,y,z = matmul(rotatex_angle,((x1,),(y1,),(0,)))
        self.changePosition((x[0],y[0]))
    def revolve(self,angle,center):
        self.current_state.rotate(angle,center)
    def move(self,tx,ty):
        self.current_state.translate(tx,ty)
    def changePosition(self,pos):
        self.pos = pos
        self.current_state.attribs.update({"x":pos[0],"y":pos[1]})
    def changeStyle(self,attribute,setting):
        self.style[attribute]=str(setting)
        self.current_state.attribs['style']=dict2style(self.style)
    def updateStyle(self,dic):
        self.style.update(dic)
        self.current_state.attribs['style']=dict2style(self.style)
    def popStyle(self,attribute):
        content = self.style.pop(attribute)
        self.current_state.attribs['style']=dict2style(self.style)
        return content.strip()
    def __str__(self):
        return self.current_state.tostring()

class Line(BaseElement):
    def __init__(self,start,end,screen,width=1,style='stroke: white;'):
        style+=';stroke-width: {0}px;'.format(width)
        super(Line,self).__init__(
            screen.line(start,end,style=style.replace(";;",";")),
            start,style,screen
        )
        self.end = end
        self.width=width
        self.size = dform(start,end)
    def center(self):
        x1,y1=self.pos
        x2,y2=self.end
        return (x1+x2)/2,(y1+y2)/2
    def changeWidth(self,n_width):
        self.changeStyle('stroke-width',str(round(n_width,3))+"px")
        self.width = n_width
    def changeSize(self,new_size):
        size = self.size
        self.size = new_size
        self.changeWidth(new_size*self.width/size)
        p1,p2 = self.pos,self.end
        d = dform(p1,p2)/2
        size/=2
        x1,y1 = p1
        cx,cy = (x1+p2[0])/2,(y1+p2[1])/2
        xl = ((cx- x1)/d)* size
        yl = ((cy- y1)/d)* size
        start,end = (cx-xl,cy-yl),(cx+xl,cy+yl)
        self.current_state.attribs.update({
            'x1':start[0],'y1':start[1],
            'x2':end[0],'y2':end[1]
            })
        self.pos,self.end = start,end
    def changePosition(self,pos):
        x1,y1 = self.pos
        self.pos = pos
        x2,y2 = pos
        x3,y3 = self.end 
        x3+=x2-x1
        y3+=y2-y1
        self.end = x3,y3
        self.current_state.attribs.update({
                'x1':x2,'y1':y2,
                'x2':x3,'y2':y3
            })
class Text(BaseElement):
    def __init__(self,text,pos,screen,style="stroke:white;",size=20):
        super(Text,self).__init__(
            screen.text(text,insert=pos,style=style),
            pos,style,screen
        )
        self.text = text
        self.changeSize(size)
    def center(self):
        x,y=self.pos
        size=self.size
        tl = len(self.text)
        return (x+(size*tl)/4,y-(size/4))
    def changeSize(self,size):
        self.changeStyle('font-size',"{0}px".format(size))
        self.size=size
        
class Rect(BaseElement):
    def __init__(self,pos,lb,screen,style='fill: white;'):
        super(Rect,self).__init__(
            screen.rect(insert=pos,size=lb),
            pos,style,screen
        )
        self.lb = lb
    def center(self):
        x,y=self.pos
        l,b=self.lb
        return (x+(l/2),y+(b/2))
    def changeSize(self,size):
        l,b =self.lb
        r  = l/b
        l=size
        b=l/r
        self.lb=l,b
        self.current_state.attribs.update({'height':l,'width':b})
class Circle(BaseElement):
    def __init__(self,center,r,screen,style='fill: white;'):
        super(Circle,self).__init__(
            screen.circle(center,r,style=style),
            center,style,screen
        ) 
        self.size = r
    def changeSize(self,size):
        self.current_state.attribs['r']=size
        self.size=size
    def changePosition(self,pos):
        #self.pos = pos
        self.current_state.attribs.update({'cx':pos[0],'cy':pos[1]})
    center = lambda:self.pos

class Ellipse(BaseElement):
    def __init__(self,center,rs,screen,style='fill: white;'):
        super(Ellipse,self).__init__(
            screen.ellipse(center,rs,style=style),
            center,style,screen
        )
        self.rs = rs
    def center(self):
        x,y = self.pos
        r1,r2 = self.rs
        return x+(r1/2),y+(r2/2)
    def changeSize(self,size):
        r1,r2 =self.rs
        c  = r1/r2
        r1=size
        r2=r1/c
        self.rs=r1,r2
        self.current_state.attribs.update({'rx':r1,'ry':r2})
    def changePosition(self,pos):
        self.pos = pos
        self.current_state.attribs.update({'cx':pos[0],'cy':pos[1]})

class Polygon(BaseElement): # Closed Polyine = Polygon
    def __init__(self,points,screen,style='fill: white;'):
        super(Polygon,self).__init__(
            screen.polygon(points,style=style),
            self.center(),style,screen
        )
        self.size = dform(self.pos,points[0])
    def center(self):
        points = self.current_state.points
        total_points = len(points)
        x,y=0,0
        for px,py in points:
            x+=px
            y+=py
        x/=total_points
        y/=total_points
        return x,y
    def changePosition(self,pos):
        points = self.current_state.points
        x1,y1 = self.pos
        x2,y2 = pos
        c1,c2 = (x2-x1),(y2-y1)
        for l,(px,py) in enumerate(points):
            points[l] = (px+c1),(py+c2)
        self.current_state.points=points
        self.pos = pos
    def changeSize(self,new_size):
        size=new_size-self.size
        center = self.pos #center
        # Increasing distance b/w center and points
        self.current_state.points = \
            [increase(center,p,size) for p in self.current_state.points]
        self.size= new_size
    def addPoints(self,points):
        self.current_state.points+=points
        self.pos = self.center()

class PolyLine(Polygon):
    def __init__(self,points,screen,style='stroke: white;'):
        super(PolyLine,self).__init__(points,screen,style=style)
        self.current_state.elementname='polyline'
