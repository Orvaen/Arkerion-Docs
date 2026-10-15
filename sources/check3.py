import traceback
from glyphs3 import GLYPHS
from directions2 import PROPOSALS
for P in PROPOSALS:
    for ch, f in GLYPHS.items():
        try: f(P)
        except Exception as e: print(P['name'], repr(ch), type(e).__name__, str(e)[:80])
