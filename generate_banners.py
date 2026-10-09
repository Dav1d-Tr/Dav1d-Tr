"""Compact F1-inspired title animation. Pillow required; all telemetry is simulated."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import math
ROOT=Path(__file__).resolve().parent;A=ROOT/'assets'
FONT_DIR=Path('/usr/share/fonts/truetype/dejavu')
W,H,N=1000,280,100
fonts={}
def font(n,b=False):
 key=(n,b)
 if key not in fonts:fonts[key]=ImageFont.truetype(str(FONT_DIR/('DejaVuSans-Bold.ttf' if b else 'DejaVuSansMono.ttf')),n)
 return fonts[key]
def txt(d,x,y,s,n=11,c='#91a3ba',b=False):d.text((x,y),s,font=font(n,b),fill=c)
path=[(620,142),(642,102),(710,79),(760,85),(779,106),(758,122),(804,137),(838,107),(914,92),(944,109),(936,151),(894,170),(849,164),(818,184),(762,173),(718,149),(666,166),(620,142)]
lens=[math.dist(a,b) for a,b in zip(path,path[1:])];total=sum(lens)
def pos(u):
 v=(u%1)*total
 for a,b,l in zip(path,path[1:],lens):
  if v<=l:return (a[0]+(b[0]-a[0])*v/l,a[1]+(b[1]-a[1])*v/l)
  v-=l
 return path[0]
base=Image.new('RGB',(W,H));d=ImageDraw.Draw(base)
for y in range(H):
 v=y/H;d.line((0,y,W,y),fill=(int(7+4*v),int(13+7*v),int(24+11*v)))
# Subtle architectural diagonal planes, no photographic backdrop.
d.polygon([(500,0),(680,0),(490,280),(310,280)],fill='#0d192a')
d.polygon([(533,0),(540,0),(350,280),(343,280)],fill='#192a3e')
d.polygon([(970,0),(1000,0),(1000,280),(790,280)],fill='#0b1523')
d.line((30,31,496,31,511,16,970,16),fill='#344255')
d.line((30,31,136,31),fill='#ff9138',width=3)
txt(d,32,45,'DR / DEVELOPMENT + DESIGN',10,'#f1a365')
txt(d,29,79,'DAVID ROZO',44,'#edf3fc',True)
txt(d,34,141,'FULL STACK DEVELOPMENT / UI & UX',13,'#b5c4d7')
# Graphic instrument band takes the place of technology names.
for y in [179,196,213]:d.line((34,y,261,y),fill='#1e2e41')
for x in range(34,262,38):d.line((x,179,x,213),fill='#1e2e41')
d.line((280,178,280,214),fill='#334258')
for j in range(3):
 x=464+j*16
 d.polygon([(x,183),(x+9,183),(x-5,208),(x-14,208)],fill='#354054' if j<2 else '#ff9138')
d.line((30,234,969,234),fill='#29394c')
txt(d,33,251,'PRECISION. PERFORMANCE. CODE.',10,'#aabbd0')
txt(d,620,47,'LAP TRACE / SIM',9,'#a5b6c9')
d.line(path,fill='#253950',width=9,joint='curve');d.line(path,fill='#8da1b9',width=2,joint='curve')
for a in range(2):
 for b in range(3):d.rectangle((614+a*5,134+b*5,618+a*5,138+b*5),fill='#e9eef5' if (a+b)%2 else '#0d1725')
frames=[]
for k in range(N):
 im=base.copy();d=ImageDraw.Draw(im);t=k/N
 # Slow sequential starting lights, then a continuous lap with a moving trail.
 launch=k<25
 # Moving telemetry curve and rev bars, without technology labels.
 pts=[]
 for j in range(114):
  value=0 if launch else 7*math.sin(j*.12-k*.22)+3*math.sin(j*.34-k*.39)
  pts.append((34+j*2,196-value))
 d.line(pts,fill='#ffab67',width=2)
 if not launch:
  px,py=pts[-1];d.ellipse((px-2,py-2,px+2,py+2),fill='#fff1df')
 for j in range(17):
  height=4 if launch else 6+int(27*(.5+.5*math.sin(k*.15+j*.3)))
  x=301+j*8
  d.rectangle((x,214-height,x+4,214),fill='#ff9138' if j>11 else '#7c96ae')
 for j in range(5):
  lit=launch and k>=j*4
  x=847+j*24
  d.ellipse((x,44,x+11,55),fill='#fc6648' if lit else '#253244',outline='#485363')
 u=0 if launch else (k-25)/75
 for j in range(18,0,-1):
  if not launch:
   x,y=pos(u-j*.003);d.ellipse((x-3,y-3,x+3,y+3),fill=(int(91+159*(1-j/19)),int(54+89*(1-j/19)),35))
 x,y=pos(u);d.ellipse((x-5,y-5,x+5,y+5),fill='#ff9c45');d.ellipse((x-2,y-2,x+2,y+2),fill='#fff6e9')
 # Short moving light streaks remain outside the name area.
 for j in range(4):
  x=555+(k*6+j*98)%430;y=211+j*4
  d.line((x,y,min(970,x+20+int(u*25)),y),fill='#465169' if launch else '#996039')
 speed=0 if launch else round(178+115*math.sin(math.pi*u)**2)
 gear='N' if launch else str(max(3,min(8,round(speed/40))))
 txt(d,620,251,f'{speed:03} KM/H',10,'#e7effa');txt(d,736,251,'GEAR '+gear,10,'#ffac6b')
 txt(d,845,251,'READY' if launch else f'SECTOR {1+min(2,int(u*3))}',10,'#aabbd0')
 # Rotating rim indicator, kept small so the banner remains compact.
 cx,cy=552,255
 d.ellipse((cx-13,cy-13,cx+13,cy+13),fill='#0a1422',outline='#e59b55',width=2)
 for j in range(5):
  a=j*math.tau/5+(0 if launch else u*math.tau*8)
  d.line((cx,cy,cx+9*math.cos(a),cy+9*math.sin(a)),fill='#9babbd',width=1)
 frames.append(im)
pal=frames[50].quantize(colors=128)
q=[f.quantize(palette=pal,dither=Image.Dither.NONE) for f in frames]
q[0].save(A/'header.gif',save_all=True,append_images=q[1:],duration=100,loop=0,disposal=1,optimize=True)
frames[58].save(A/'header-static.png');frames[58].save(ROOT.parent/'compact-review.png')
print('Compact banner:',W,H,'100 frames;', (A/'header.gif').stat().st_size,'bytes')
