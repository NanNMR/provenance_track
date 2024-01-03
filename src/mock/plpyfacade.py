import configparser
from collections.abc import Mapping
from typing import Optional

import yaml
from postgresql_access import DatabaseDict

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
        g = globals()
        for d in ('GD','SD'):
            if getattr(g,d,None) is None:
                g[d] = {}
        self.conn = self.db.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        MockPlpy._instance = None
        self.conn.close()
        self.conn = None

    def set_trigger_data(self,old:Optional[Mapping],_new:Optional[Mapping]):
        raise NotImplementedError()
#        td = {}
#        if old is not None:
#            td['old'] = old
#        if _new is not None:
#            td['new'] = n = copy.deepcopy(_new)
#            if old is not None:
#                for k, v in old:
#                    if k not in n:
#                        n[k] = v




