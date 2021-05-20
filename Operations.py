from svgwrite import gradients
from utils import *
lingrad = gradients.LinearGradient
class Animate:
    def __init__(self,obj):
        self.object = obj
    def zoom(self,times,frame=1):
        obj = self.object
        attribs =  obj.current_state.attribs
        size=10
        if 'size' in dir(obj):
            size=obj.size
        elif 'size' in attribs:
            size = attribs['size']
        elif 'height' in attribs:
            size = attribs['height']
        inc = ((times*size)-size)/frame
        for _ in range(frame):
            size+=inc
            obj.changeSize(size)
            yield obj.current_state
    def rotate(self,angle,frame=1):
        obj = self.object
        inc = angle/frame
        cangle =0
        for _ in range(frame):
            cangle+=inc
            obj.rotate(cangle)
            yield obj.current_state
    def flip(self,angle,frame=1):
        obj = self.object
        inc = angle/frame
        cangle =0
        for _ in range(frame):
            cangle+=inc
            obj.flip(cangle)
            yield obj.current_state
    def revolve(self,angle,center,frame=1):
        obj = self.object
        cangle  = 0
        inc = angle/frame
        for _ in range(stepsize):
            cangle+=inc
            obj.revolve(cangle,center)
            yield obj.current_state
    def moveto(self,pos,frame=1):
        obj = self.object
        x1,y1 = obj.pos
        x2,y2 = pos
        i1 = (x2-x1)/frame
        i2 = (y2-y1)/frame
        for _ in range(frame):
            x1,y1 = x1+i1,y1+i2
            obj.changePosition((x1,y1))
            yield obj.current_state
        obj.changePosition(pos)
        yield obj.current_state
    def move(self,pos,frame=1):
        obj = self.object
        i1 = pos[0]/frame
        i2 = pos[1]/frame
        x,y = 0,0
        for _ in range(frame):
            x+=i1
            y+=i2
            obj.move(x,y)
            yield obj.current_state
    def changeAttribute(self,attribute,changes):
        obj = self.object
        for change in changes:
            obj.changeAttribute(attribute,change)
            yield obj.current_state
    def fadein(self,frame=1):
        obj = self.object
        inc = .99/frame
        o=0
        for i  in range(frame):
            o+=inc
            obj.changeStyle('opacity',o)
            yield obj.current_state
    def fadeout(self,frame=1):
        obj = self.object
        inc = .99/frame
        o=1
        for i in range(frame):
            o-=inc
            obj.changeStyle('opacity',o)
            yield obj.current_state
    def strokein(self,frame=1,top=0):
        obj = self.object
        screen = obj.screen
        inc = 100/frame
        o=0
        attribs  = obj.current_state.attribs
        #Checking fill in style and object attributes(else 'white')
        fill = attribs.pop("stroke") \
              if "stroke" in attribs\
              else \
                    (obj.popStyle("stroke")
                    if "stroke" in obj.style 
                    else "white")
        obj.changeAttribute('stroke','url(#creation3)')
        if top:
            x2,y2="0%","100%"
        else:
            x2,y2= "100%","0%"
            
        lg = lingrad(id="creation3",x2=x2,y2=y2)
        screen.add(lg)
        for i in range(frame):
            o+=inc
            lg.elements=[]
            lg.add_stop_color(offset=str(round(o,3))+"%",opacity=1,color=fill)\
              .add_stop_color(offset=str(round(o,3))+"%",opacity=0,color=fill)
            yield obj.current_state
        attribs['stroke']=fill
        screen.elements.remove(lg)
    def create(self,frame=3,stroke=1):
        p3=int(frame/3)
        if stroke:
            for f in self.strokein(int(p3)): yield f
        else:
            for f in self.fadein(int(p3)): yield f
        frame = int(p3*2)
        obj = self.object
        screen = obj.screen
        inc2 = 100/frame
        inc1 = inc2*1.5
        o1=0
        o2=0
        attribs  = obj.current_state.attribs
        #Checking fill in style and object attributes(else 'white')
        fill = attribs.pop("fill") \
              if "fill" in attribs\
              else \
                    (obj.popStyle("fill")
                    if "fill" in obj.style 
                    else "white")
        obj.changeAttribute('fill','url(#creation3)')
        lg = lingrad(id="creation3")
        screen.add(lg)
        for i in range(frame):
            if o1<100:
                o1+=inc1
                o2+=inc2
            else:
                o2+=inc2
            lg.elements=[]
            lg.add_stop_color(offset=str(round(o2,3))+"%",opacity=1,color=fill)\
              .add_stop_color(offset=str(round(o1,3))+"%",opacity=0,color=fill)
            yield obj.current_state
        attribs['fill']=fill
        screen.elements.remove(lg)
    def wait(self,frame):
        obj= self.object
        for _ in range(frame):
            yield obj.current_state