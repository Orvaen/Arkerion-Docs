import sys
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from proof import to_path
from geom import translate, flatten
from glyphs3 import GLYPHS
from directions2 import PROPOSALS
S='/tmp/claude-0/-home-claude/e93b073a-487b-5439-beb3-56b3fd2d7d27/scratchpad/'
P=PROPOSALS[int(sys.argv[1])]
chars=sys.argv[2]
fig,axes=plt.subplots(1,len(chars),figsize=(4*len(chars),5))
for ax,ch in zip(axes if len(chars)>1 else [axes],chars):
    c=GLYPHS[ch](P)
    ax.add_patch(PathPatch(to_path(c),fc='#bbb',ec='none'))
    for cc in c:
        pts=flatten(cc); xs=[p[0] for p in pts]+[pts[0][0]]; ys=[p[1] for p in pts]+[pts[0][1]]
        ax.plot(xs,ys,lw=.8)
    ax.set_aspect('equal'); ax.autoscale(); ax.set_title(ch)
fig.tight_layout(); fig.savefig(S+'outl.png',dpi=60)
