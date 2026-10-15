import sys
from PIL import Image, ImageDraw, ImageFont
S='/tmp/claude-0/-home-claude-arkerion-docs/e93b073a-487b-5439-beb3-56b3fd2d7d27/scratchpad/'
size=int(sys.argv[2]); lines=sys.argv[3].split('|')
fonts=['source/ArkerionStudy-1-Atelier.otf','build/ArkerionSans-Regular-v2.otf']
h=int(size*1.25)
im=Image.new('L',(1500,h*len(lines)*2+30),255); d=ImageDraw.Draw(im)
for k,f in enumerate(fonts):
    F=ImageFont.truetype(f,size,layout_engine=ImageFont.Layout.RAQM)
    for i,l in enumerate(lines): d.text((16,8+(k*len(lines)+i)*h+k*20),l,font=F,fill=0)
im.save(S+sys.argv[1])
