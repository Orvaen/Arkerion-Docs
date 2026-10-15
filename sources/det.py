import sys
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from proof2 import setw, S
from directions2 import PROPOSALS, build
t=sys.argv[1]
fig,axes=plt.subplots(1,3,figsize=(18,5))
for ax,P in zip(axes,PROPOSALS):
    G,K=build(P); mx=setw(ax,G,K,t,0,0,True)
    for h in (0,P['xh'],P['cap']): ax.plot([-20,mx+20],[h,h],lw=.4,c='#59f')
    ax.set_aspect('equal');ax.axis('off');ax.set_xlim(-20,mx+20);ax.set_ylim(-30,760);ax.set_title(P['name'])
fig.tight_layout();fig.savefig(S+sys.argv[2],dpi=int(sys.argv[3]) if len(sys.argv)>3 else 55)
