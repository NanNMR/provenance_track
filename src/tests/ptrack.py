#!/usr/bin/env python3
import argparse
import datetime
import logging
import os
import zoneinfo


tz = zoneinfo.ZoneInfo('America/New_York')
os.environ['NO_PROVENANCE_TRACK_LOG'] = "1"
import provenance_track

from src.mock.plpyfacade import MockPlpy


def test_one(plpy):
    return plpy.make_trigger_data('public', 'pdata', 'DELETE', {'id': 1, 'name': 'bob'}, {'name': 'Mary'})


def test_two(plpy):
    bvalue = False
    return plpy.make_trigger_data('public', 'sample', 'INSERT', None,
                              {'id': 1, 'count': 5, 'description':'adding','created': datetime.datetime.now(tz=tz),
                               'good': bvalue})
def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-l', '--loglevel', default='INFO', help="Python logging level")
    parser.add_argument('yaml',nargs='?', default='ftest.yaml',help="YAML")

    args = parser.parse_args()
#    provenance_track_logger.setLevel(getattr(logging,args.loglevel))
    with MockPlpy.from_yaml_file(args.yaml) as plpy:
        from provenance_track import provenance_track_logger, record
        provenance_track_logger.addHandler(logging.StreamHandler())
        import provenance_track
        provenance_track.logsetup.set_loglevel(args.loglevel)

        #record(plpy,test_one(plpy))
        record(plpy,test_two(plpy))



if __name__ == "__main__":
    main()
