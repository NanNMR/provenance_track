from typing import Any
from pathlib import Path
import inspect
import os
try:
    import plpy
except ImportError:
    pass

class NANException(BaseException):
    pass

def _showdoc(x,out):
    if (d := getattr(x,'__doc__',None)) is not None:
        print(d,file=out)

def _explore(thing:Any,out):
#    print(thing.__name__,file=out)
    try:
        print(help(thing),file=out)
    except:
        pass
    print(type(thing),file=out)
    _showdoc(thing,out)
    if (fa := getattr(thing,'__file__',None)) is not None:
        print(f"file: {fa}",file=out)
    for d in dir(thing):
        print(d,file=out)
    for n,v in inspect.getmembers(thing):
        print(f"{n} is {v}",file=out)
    print(file=out)



def explore(thing:Any):
    with open(Path('/tmp') / f"explore{os.getpid()}",'a') as f:
        _explore(thing,f)

def failit():
    raise NANException("failure")

def nan_user()->str:
    r = plpy.execute("select current_setting('nan.user')")
    explore(r)
    return r[0]['current_setting']
