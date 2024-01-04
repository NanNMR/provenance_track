from typing import Any
from pathlib import Path
import inspect
import os

from provenance_track import PlpyAPI

try:
    import plpy
except ImportError:
    pass

class NANException(BaseException):
    pass

def opener(path, flags):
    return os.open(path, flags,mode=0o644)

def _showdoc(x,out):
    print("doc?", file=out)
    if (d := getattr(x,'__doc__',None)) is not None:
        print(d,file=out)
    else:
        print(f'{type(x)} has no __doc__',file=out)


def _explore(thing:Any,out):
#    print(thing.__name__,file=out)
    print(f"API good {isinstance(plpy,PlpyAPI)}",file=out)
    print(f"pid is: {os.getpid()}",file=out)
    print(type(thing),file=out)
    _showdoc(thing,out)
    print("file?", file=out)
    if (fa := getattr(thing,'__file__',None)) is not None:
        print(f"file: {fa}",file=out)
#    for d in dir(thing):
#        print(d,file=out)
    print("inspect", file=out)
    for n,v in inspect.getmembers(thing):
        print(f"{n} is {v}",file=out)
    print(file=out)



def explore(thing:Any):
    logname = Path('/tmp') / f"explore{os.getpid()}"
    with open(logname, 'a', opener=opener) as f:
        _explore(thing,f)
    os.chmod(logname,mode=0o644)

def failit():
    raise NANException("failure")

def nan_user()->str:
    r = plpy.execute("select current_setting('nan.user')")
    explore(r)
    return r[0]['current_setting']
