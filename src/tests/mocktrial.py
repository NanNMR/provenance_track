#!/usr/bin/env python3
import argparse
import logging

from mock.plpyfacade import MockPlpy
from provenance_track import provenance_track_logger


def main():
    logging.basicConfig()
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-l', '--loglevel', default='INFO', help="Python logging level")
    parser.add_argument('yaml',nargs='?', default='ftest.yaml',help="YAML")

    args = parser.parse_args()
    provenance_track_logger.setLevel(getattr(logging,args.loglevel))
    with MockPlpy.from_yaml_file(args.yaml) as plpy:
        r = plpy.execute('select name from public.pdata',2)
        plpy.info(r[0]['name'])
        plpy.info(r[1]['name'])
        try:
            plpy.info(r[2]['name'])
            raise ValueError("Missing IndexError")
        except IndexError:
            pass
        try:
            plpy.info(r[0]['namex'])
            raise ValueError("Missing KeyError")
        except KeyError:
            pass



if __name__ == "__main__":
    main()
