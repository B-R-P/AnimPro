from svgwrite import Drawing
from Operations import Animate
from Objects import *
from tqdm import tqdm
from subprocess import Popen,call
from os import system
from tempfile import gettempdir
tempdir = gettempdir()
system(' '.join(('cd',tempdir,'&& IF NOT EXIST animpro_temp mkdir animpro_temp')))
tempdir+="\\animpro_temp\\"
def genScreen(max_h,max_w,background):
    screen= Drawing(
        "",
        size=(str(max_h)+'px',str(max_w)+'px'),
        viewBox="0 0 {0} {1}".format(max_h,max_w)
    )
    screen.add(screen.rect(insert=(0,0),size=(max_h,max_w),id="background"))
    screen.defs.add(screen.style("backgorund{fill: "+background+";}"))
    return screen
def saveframes(screen,frames,framepos):
    cframepos=0
    for objs in zip(*frames):
        cframepos+=1
        framepos+=1
        screen.elements+=objs
        screen.saveas(tempdir+"frame{0}.svg".format(framepos))
        for f in objs:
            screen.elements.remove(f)
    return framepos

class Scene:
    def __init__(self,max_h,max_w,background="black"):
        self.screen = genScreen(max_h,max_w,background)
        self.framepos = 0
    def render(self,*frames):
        frames =  [combineGen(objs) if isinstance(objs, tuple) else objs for objs in frames]
        self.framepos = saveframes(self.screen,frames,self.framepos)
    def render_video(self,filename):
        print('Creating TIF Files')
        converts = [(i,f'sconvert {tempdir}frame{i}.svg {tempdir}frame{i}.tif') for i in range(1,self.framepos+1)]
        previous = []
        for l,program in tqdm(converts):
            previous.append(Popen(program))
            if l%4==0:
                for p in previous:
                    p.wait()
                previous = []
        for p in previous:
            p.wait()
        print('Converting TIF files into',filename)
        call([
            'ffmpeg','-hide_banner','-loglevel','error',
            '-y','-start_number','1','-i',
            tempdir+'frame%d.tif','-r',
            '60','-b:v','5000k',filename
        ])
        system(' '.join(('cd',tempdir,'&&','del','/Q','*')))
        print('Opening',filename)
