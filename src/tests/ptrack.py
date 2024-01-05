#!/usr/bin/env python3
import argparse
import logging
import sys

from mock.plpyfacade import MockPlpy
from provenance_track import provenance_track_logger, record



def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-l', '--loglevel', default='INFO', help="Python logging level")
    parser.add_argument('yaml',nargs='?', default='ftest.yaml',help="YAML")

    args = parser.parse_args()
    provenance_track_logger.setLevel(getattr(logging,args.loglevel))
    with MockPlpy.from_yaml_file(args.yaml) as plpy:
        plpy.set_trigger_data('public','pdata',{'id':1, 'name':'Mary'}, {'name':'bob'})
        record(plpy)



if __name__ == "__main__":
    main()
