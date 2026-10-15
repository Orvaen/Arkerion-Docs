import sys
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from proof import to_path
from geom import translate
from directions2 import PROPOSALS, build

S = '/tmp/claude-0/-home-claude/e93b073a-487b-5439-beb3-56b3fd2d7d27/scratchpad/'


def setw(ax, G, K, text, x, y, guides=False, kern_on=True):
    prev = None
    for ch in text:
        if prev and kern_on:
            x += K.get(prev + ch, 0)
        g = G[ch]
        if guides:
            ax.add_patch(plt.Rectangle((x, y - 220), g['adv'], 1000, fill=False, lw=0.3, ec='#d55'))
        ax.add_patch(PathPatch(to_path(translate(g['c'], x, y)), fc='#111', ec='none'))
        x += g['adv']; prev = ch
    return x


if __name__ == '__main__':
    texts = sys.argv[1].split('|')
    guides = '-g' in sys.argv
    built = [build(P) for P in PROPOSALS]
    fig, axes = plt.subplots(3, 1, figsize=(15, 3.2 * len(texts) + 0.6))
    for ax, P, (G, K) in zip(axes, PROPOSALS, built):
        y = 0; maxx = 0
        for t in texts:
            maxx = max(maxx, setw(ax, G, K, t, 0, y, guides))
            if guides:
                for h in (0, P['xh'], P['cap']):
                    ax.axhline(y + h, lw=.3, c='#59f')
            y -= 1000
        ax.set_aspect('equal'); ax.axis('off')
        ax.set_xlim(-40, max(maxx, 3000) + 40); ax.set_ylim(y + 750, 790)
        ax.set_title('%s   kern %s' % (P['name'], K), loc='left', fontsize=9)
    fig.tight_layout(); fig.savefig(S + sys.argv[2], dpi=int(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[3].isdigit() else 60)
