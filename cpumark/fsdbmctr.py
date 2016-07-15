__author__ = 'followcat'

import fsdbm


def init_dbset():
    cpudb = fsdbm.FSDBM('FSDBM/cpu_fsdbm.fdb')
    gpudb = fsdbm.FSDBM('FSDBM/gpu_fsdbm.fdb')
    picdb = fsdbm.FSDBM('FSDBM/pic_fsdbm.fdb')
    markdb = fsdbm.FSDBM('FSDBM/mark_fsdbm.fdb')
    mapdb = fsdbm.FSDBM('FSDBM/map_fsdbm.fdb')
    return cpudb, gpudb, picdb, markdb, mapdb

cpudb, gpudb, picdb, markdb, mapdb = init_dbset()

def dbinserterCpuGpuMark(table, model, mark, rank, value, price):
    if table == 'CpuMark':
        db = cpudb
    elif table == 'GpuMark':
        db = gpudb
    db[model] = {
        'mark': mark,
        'rank': rank,
        'value': value,
        'price': price
        }


def dbinserterGameMarkPic(table, Game, url):
    picdb[Game] = {
        'url': url
    }


def dbinserterGpuGameOptionFPS(table, model, Game, Options, FPS):
    if model not in markdb:
        markdb[model] = []
    markdb[model] = markdb[model] + [{
        'game': Game,
        'options': Options,
        'FPS': FPS
    }]


def dbinserterGameMarkMapping(model, Mapping, Mult):
    mapdb[model] = {
        'mapping': Mapping,
        'mult': Mult,
    }
