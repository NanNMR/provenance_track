import configparser
import copy
import sys
from collections.abc import Mapping
from typing import Optional, Dict

import yaml
from postgresql_access import DatabaseDict


def create_global_symbol(name,value):
    """Create symbol in global (bultin) namespace"""
    gs = sys.modules['builtins'].__dict__
    if (gs.get(name,None)) is None:
        gs[name] = value
        return
    raise ValueError(f"{name} already present")

create_global_symbol('GD',{})

from provenance_track import PlpyAPI, PyResult, provenance_track_logger

class MockResult(PyResult):


    class RowProxy:
        def __init__(self,parent,row):
            self.parent = parent
            self.row = row

        def __getitem__(self, item):
            return self.parent.get_result(self.row,item)

    def __init__(self,cursor,limit):
        self.colnames = [d[0] for d in cursor.description]
        if limit is None:
            self.data = cursor.fetchall()
        else:
            self.data = cursor.fetchmany(size=limit)

    def __iter__(self):
        pass

    def __len__(self):
        return len(self.data)

    def __getitem__(self, row):
        assert isinstance(row,int)
        if row >= len(self.data):
            raise IndexError()
        return MockResult.RowProxy(self,row)

    def nrows(self):
        return len(self.data)

    def get_result(self,row,item):
        assert isinstance(row,int)
        assert row <= len(self.data)
        try:
            col = self.colnames.index(item)
        except ValueError:
            raise KeyError()
        return self.data[row][col]


class MockPlpy(PlpyAPI):

    _instance = None


    @staticmethod
    def execute(query: str, limit: Optional[int] = None) -> PyResult:
        with MockPlpy._instance.conn.cursor() as curs:
            provenance_track_logger.debug(query)
            curs.execute(query)
            return MockResult(curs,limit)

    @staticmethod
    def info(s: str) -> None:
        provenance_track_logger.info(s)


    def __init__(self,cdata:Mapping,application_name:str):
        self.db = DatabaseDict(dictionary=cdata)
        self.db.set_app_name(application_name)
        self.conn = None

    @staticmethod
    def from_config_file(config_file):
        with configparser.ConfigParser() as config:
            config.read(config_file)
            return MockPlpy(config,"mock-plpy")

    @staticmethod
    def from_yaml_file(file):
        with open(file) as f:
            c = yaml.safe_load(f)
            return MockPlpy(c['database'],"mock-plpy")


    def __enter__(self):
        MockPlpy._instance = self
        create_global_symbol('SD',{})
        self.conn = self.db.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        MockPlpy._instance = None
        self.conn.close()
        self.conn = None

    def set_trigger_data(self,schema,table,event,old:Optional[Dict],_new:Optional[Dict]):
        assert event in ('INSERT','UPDATE','DELETE','TRUNCATE')
        td = {'table_name':table,'schema_name':schema,'event':event}
        if old is not None:
            td['old'] = old
        if _new is not None:
            td['new'] = n = copy.deepcopy(_new)
            if old is not None:
                for k, v in old.items():
                    if k not in n:
                        n[k] = v
        create_global_symbol('TD',td)



