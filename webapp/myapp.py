import json

from flask import Flask, request
from flask import render_template

from cpumark.fsdbmctr import *


app = Flask(__name__)
app.debug = True


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/GetNameList',methods=['GET'])
def GetNameList():
    rs = []
    table = request.args.get('table')
    if table == 'CpuMark':
        rs = cpudb.keys()
    elif table == 'GpuMark':
        rs = gpudb.keys()
    return json.dumps(rs, ensure_ascii=False, encoding='utf-8')


@app.route('/GetHardList',methods=['GET'])
def GetHardList():
    table = request.args.get('table')
    if table == 'CpuMark':
        rs = cpudb.keys()
    elif table == 'GpuMark':
        rs = gpudb.keys()
    return json.dumps(rs, ensure_ascii=False, encoding='utf-8')

    
@app.route('/GetOneData',methods=['GET'])
def GetOneData():
    table = request.args.get('table')
    model = request.args.get('hardname')
    if table == 'CpuMark':
        rs = cpudb[model]
    elif table == 'GpuMark':
        rs = gpudb[model]
    return json.dumps(rs, ensure_ascii=False, encoding='utf-8')


@app.route('/GetGamePic',methods=['GET'])
def GetGamePic():
    gamename = request.args.get('gamename')
    rs = picdb[gamename]['url']
    return json.dumps(rs, ensure_ascii=False, encoding='utf-8')


@app.route('/GetGpuFps',methods=['GET'])
def GetGpuFps():
    model = request.args.get('gpuname')
    gpudb[model]

    map_gpu = mapdb[model]['mapping']
    mult = mapdb[model]['mult']

    ans = {'map':map_gpu, 'mult':mult, 'fps':[]}
    result = markdb[map_gpu]
    for each in result:
        ans['fps'].append(each)
    return json.dumps(ans, ensure_ascii=False, encoding='utf-8')


app.run(port=8886)
