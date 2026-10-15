import sys
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from proof import set_text
from directions import DIRECTIONS
S='/tmp/claude-0/-home-claude/e93b073a-487b-5439-beb3-56b3fd2d7d27/scratchpad/'
idx=[int(i) for i in sys.argv[1].split(',')]
fig, axes = plt.subplots(len(idx),1, figsize=(18, 5*len(idx)))
if len(idx)==1: axes=[axes]
for ax,i in zip(axes,idx):
    P=DIRECTIONS[i]
    x=set_text(ax,P,'ARKEION',0,0,guides=True)
    set_text(ax,P,'arkeion',x+200,0,guides=True)
    for h in (0,P['xh'],P['cap']): ax.axhline(h,lw=.4,c='#59f')
    ax.set_aspect('equal'); ax.axis('off'); ax.set_xlim(-50, 8000); ax.set_ylim(-60, 800)
    ax.set_title(P['name'],loc='left')
fig.tight_layout(); fig.savefig(S+sys.argv[2],dpi=60)
