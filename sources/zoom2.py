import sys
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from proof import set_text
from directions import DIRECTIONS
S='/tmp/claude-0/-home-claude/e93b073a-487b-5439-beb3-56b3fd2d7d27/scratchpad/'
txt=sys.argv[1]
fig, axes = plt.subplots(3,1, figsize=(14, 13))
for ax,P in zip(axes,DIRECTIONS):
    x=set_text(ax,P,txt,0,0,guides=True)
    for h in (0,P['xh'],P['cap']): ax.axhline(h,lw=.4,c='#59f')
    ax.set_aspect('equal'); ax.axis('off'); ax.set_xlim(-50, x+50); ax.set_ylim(-60, 780)
    ax.set_title(P['name'],loc='left')
fig.tight_layout(); fig.savefig(S+sys.argv[2],dpi=55)
