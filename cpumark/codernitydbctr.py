__author__ = 'followcat'

from CodernityDB.database import Database
from CodernityDB.hash_index import HashIndex


class WithXIndex(HashIndex):

    def __init__(self, dbpath, keyname, *args, **kwargs):
        kwargs['key_format'] = '?'
        self.dbpath = dbpath
        self.keyname = keyname
        super(WithXIndex, self).__init__(dbpath, keyname, *args, **kwargs)

    def make_key_value(self, data):
        a_val = data.get(self.keyname)
        if a_val is not None:
            return a_val, None
        return None

    def make_key(self, key):
        return key


def init_dbset():
    db = Database('Database')
    db.create()
    inx_1 = WithXIndex(db.path, 'table')
    inx_2 = WithXIndex(db.path, 'model')
    #inx_3 = WithXIndex(db.path, 'rank')
    #inx_4 = WithXIndex(db.path, 'game')
    #inx_5 = WithXIndex(db.path, 'options')
    db.add_index(inx_1)
    db.add_index(inx_2)
    #db.add_index(inx_3)
    #db.add_index(inx_4)
    #db.add_index(inx_5)


def dbinserterCpuGpuMark(table, model, mark, rank, value, price):
    data = dict()
    data = {
        'table': table,
        'model': model,
        'mark': mark,
        'rank': rank,
        'value': value,
        'price': price
    }
    db = Database('Database')
    db.open()
    db.insert(data)


def dbinserterGameMarkPic(table, Game, url):
    data = dict()
    data = {
        'table': table,
        'game': Game,
        'url': url
    }
    db = Database('Database')
    db.open()
    db.insert(data)


def dbinserterGpuGameOptionFPS(table, model, Game, Options, FPS):
    data = dict()
    data = {
        'table': table,
        'model': model,
        'game': Game,
        'options': Options,
        'FPS': FPS
    }
    db = Database('Database')
    db.open()
    db.insert(data)


def dbinserterGameMarkMapping(table, model, Mapping, Mult):
    data = dict()
    data = {
        'table': table,
        'model': model,
        'mapping': Mapping,
        'mult': Mult,
    }
    db = Database('Database')
    db.open()
    db.insert(data)

init_dbset()
