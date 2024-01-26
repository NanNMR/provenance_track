#!/usr/bin/env python3
import argparse
import logging
import sys

from provenance_track import provenance_track_logger, record
from postgresql_access import DatabaseDict

class TableMaker:

    def __init__(self,config):
        self.db = DatabaseDict(dictionary=config)

    def createTable(self,name):
        if '.' in name:
            schema, table = name.split('.')
        else:
            schema = 'public'
            table=name
        with self.db.connect(application_name='create provenance name') as conn:
            with conn.cursor() as curs:
                curs.execute('select pg_get_tabledef(%s,%s,,false)',(schema,table))
                definition = curs.fetchone()[0]
                print(definition)




def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-l', '--loglevel', default='INFO', help="Python logging level")
    parser.add_argument('--yaml',default='local.yaml',help="YAML")
    parser.add_argument('table name',help="table name [schema.table]")

    args = parser.parse_args()
    provenance_track_logger.setLevel(getattr(logging,args.loglevel))



if __name__ == "__main__":
    main()
