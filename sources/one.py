import sys
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from proof2 import setw, S
from directions2 import PROPOSALS, build
i=int(sys.argv[1]); P=PROPOSALS[i]; G,K=build(P)
texts=sys.argv[2].split('|'); g='-g' in sys.argv
fig,ax=plt.subplots(figsize=(14, 2.6*len(texts)))
y=0;mx=0
for t in texts:
    mx=max(mx,setw(ax,G,K,t,0,y,g))
    if g:
        for h in (0,P['xh'],P['cap']): ax.plot([-40,mx+40],[y+h,y+h],lw=.4,c='#59f')
    y-=1000
ax.set_aspect('equal');ax.axis('off');ax.set_xlim(-40,mx+40);ax.set_ylim(y+760,780)
fig.tight_layout();fig.savefig(S+'one%d.png'%i,dpi=50)
