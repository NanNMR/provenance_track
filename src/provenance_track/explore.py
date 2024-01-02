from typing import Any
from pathlib import Path
import os


def _explore(thing:Any,out):
    print(type(thing),file=out)
    if (fa := getattr(thing,'__file__',None)) is not None:
        print(f"file: {fa}",file=out)
    for d in dir(thing):
        print(d,file=out)



def explore(thing:Any):
    with open(Path('/tmp') / f"explore{os.getpid()}",'w') as f:
        _explore(thing,f)
