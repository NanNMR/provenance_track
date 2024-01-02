import sys

from provenance_track.explore import _explore, explore

x = 7
_explore(x,sys.stdout)

explore(x)