import sys, glob
from PIL import Image, ImageDraw, ImageFont
S='/tmp/claude-0/-home-claude/e93b073a-487b-5439-beb3-56b3fd2d7d27/scratchpad/'
i=int(sys.argv[1]); size=int(sys.argv[2]); lines=sys.argv[3].split('|')
f=sorted(glob.glob('out3/*.otf'))[i]
F=ImageFont.truetype(f,size)
h=int(size*1.35)
im=Image.new('L',(1500,h*len(lines)+20),255); d=ImageDraw.Draw(im)
for j,t in enumerate(lines): d.text((16,10+j*h),t,font=F,fill=0)
im.save(S+sys.argv[4])
