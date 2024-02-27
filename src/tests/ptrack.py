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
    return plpy.make_trigger_data('public', 'pdata', 'INSERT',
                          {'id': 2, 'name': 'bob',
                           'state': {'orig':None, 'usr':None, 'is_user':False}}, {'name': 'Mary'})

def test_two(plpy):
    bvalue = False
    return plpy.make_trigger_data('public', 'psample', 'INSERT', None,
                              {'id': 1,
                               'count': 5,
                               'description':'adding',
                               'created': datetime.datetime.now(tz=tz),
                               'good': bvalue,
                               'stuff':['a','b'],
                               'hydration_unit':'mg',
                               'pdate': datetime.date(year=2024,month=2,day=3),
                               }
                                  )
def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-l', '--loglevel', default='INFO', help="Python logging level")
    parser.add_argument('yaml',nargs='?', default='ftest.yaml',help="YAML")
    parser.add_argument('--supported',action='store_true',help="List supported types")

    args = parser.parse_args()
#    provenance_track_logger.setLevel(getattr(logging,args.loglevel))
    with MockPlpy.from_yaml_file(args.yaml) as plpy:
        from provenance_track import provenance_track_logger, record, supported_types
        if args.supported:
            print(supported_types())
        provenance_track_logger.addHandler(logging.StreamHandler())
        import provenance_track
        provenance_track.logsetup.set_loglevel(args.loglevel)

        record(plpy,test_one(plpy))
        #record(plpy,test_two(plpy))



if __name__ == "__main__":
    main()
