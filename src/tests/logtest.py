#!/usr/bin/env python3
import argparse
import datetime
import logging
import zoneinfo

import provenance_track.logsetup

tz = zoneinfo.ZoneInfo('America/New_York')
import provenance_track



def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-l', '--loglevel', default='WARNING', help="Python logging level")
    parser.add_argument('level',help="Message level")
    parser.add_argument('message',nargs='*',help="msg")

    args = parser.parse_args()
    provenance_track.logsetup.set_loglevel(args.loglevel)
    lvl = getattr(logging,args.level)
    provenance_track.provenance_track_logger.log(lvl,' '.join(args.message))



if __name__ == "__main__":
    main()
