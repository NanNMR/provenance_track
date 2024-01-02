from typing import Any
from pathlib import Path
import inspect
import os


def _showdoc(x,out):
    if (d := getattr(x,'__doc__',None)) is not None:
        print(d,file=out)

def _explore(thing:Any,out):
#    print(thing.__name__,file=out)
    print(type(thing),file=out)
    _showdoc(thing,out)
    if (fa := getattr(thing,'__file__',None)) is not None:
        print(f"file: {fa}",file=out)
    for d in dir(thing):
        print(d,file=out)
    for n,v in inspect.getmembers(thing):
        print(f"{n} is {v}",file=out)



def explore(thing:Any):
    with open(Path('/tmp') / f"explore{os.getpid()}",'w') as f:
        _explore(thing,f)
