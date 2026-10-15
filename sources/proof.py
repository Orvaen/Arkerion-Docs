import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch
from geom import translate
from glyphs import GLYPHS
from directions import DIRECTIONS


def to_path(contours):
    verts, codes = [], []
    for p0, segs in contours:
        verts.append(p0); codes.append(Path.MOVETO)
        for s in segs:
            if s[0] == 'L':
                verts.append(s[1]); codes.append(Path.LINETO)
            else:
                verts += [s[1], s[2], s[3]]; codes += [Path.CURVE4] * 3
        verts.append(p0); codes.append(Path.CLOSEPOLY)
    return Path(verts, codes)


def set_text(ax, P, text, x0, y0, kern=None, color='#111', guides=False):
    x = x0
    for ch in text:
        if ch == ' ':
            x += 240; continue
        cs, adv = GLYPHS[ch](P)
        if guides:
            ax.add_patch(plt.Rectangle((x, y0 - 250), adv, 1050, fill=False, lw=0.3, ec='#c55'))
        ax.add_patch(PathPatch(to_path(translate(cs, x, y0)), fc=color, ec='none'))
        x += adv
    return x


def proof(out, guides=False):
    rows = ['ARKERION', 'Arkerion', 'AREKION ARKERION', 'arkerion oneiro', 'nonorneka']
    fig, axes = plt.subplots(len(DIRECTIONS), 1, figsize=(16, 6 * len(DIRECTIONS)))
    for ax, P in zip(axes, DIRECTIONS):
        y = 0
        for t in rows:
            set_text(ax, P, t, 0, y, guides=guides)
            if guides:
                for h in (0, P['xh'], P['cap']):
                    ax.axhline(y + h, lw=0.3, c='#59f')
            y -= 1100
        ax.set_xlim(-100, 9000); ax.set_ylim(y + 600, 900)
        ax.set_aspect('equal'); ax.axis('off')
        ax.set_title(P['name'], loc='left', fontsize=16)
    fig.tight_layout()
    fig.savefig(out, dpi=70)


if __name__ == '__main__':
    proof(sys.argv[1] if len(sys.argv) > 1 else 'proof.png', guides='-g' in sys.argv)
