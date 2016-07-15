# -*- coding: utf-8 -*-
import os
import re
import fsdbmctr as dbctr
from pyquery import PyQuery as pq


def file_reader(filename):
    data = open(filename)
    return data.read( )


def eachcpu_processer(table_name, eachcpu_data):
    td_list = eachcpu_data.find('td')
    temp_arr = []
    for i in range(0,td_list.length):
        try:
            if i == 0:
                temp_arr.append(td_list.eq(i).text())
            elif i == 1:
                temp_arr.append(int(td_list.eq(i).text()))
            elif i == 2:
                try:
                    temp_arr.append(int(td_list.eq(i).text()))
                except ValueError:
                    temp_arr.append(td_list.eq(i).text())
            elif i == 3:
                temp_arr.append(td_list.eq(i).text())
            elif i == 4:
                temp_arr.append(td_list.eq(i).text())
        except UnicodeDecodeError:
            print "jump"
            return
    print temp_arr
    dbctr.dbinserterCpuGpuMark(table_name, temp_arr[0],temp_arr[1],temp_arr[2],temp_arr[3],temp_arr[4])


def cpu_processer(table_name, cpu_webpage):
    data = file_reader(cpu_webpage)
    pydata = pq(data)
    tr_collect = pydata.find('#cputable tbody tr')

    for i in range(0,tr_collect.length-1):
        eachcpu_processer(table_name, tr_collect.eq(i))


def insert_gamepic(game_arr):
    for each in game_arr:
        dbctr.dbinserterGameMarkPic("GamePic", each[0].encode('utf-8'), each[1])


def gamemark_header_processer(header, headersetting):
    j = 0
    setting_arr = []
    setting_arr.append([])
    td_collect = headersetting.find('td')
    print headersetting.find('.tx-nbc2fe-gpulist-image')
    for i in range(0, td_collect.length-2):
        if len(td_collect.eq(i).text())  == 0:
            j += 1
            setting_arr.append([])
        else:
            setting_arr[j].append(td_collect.eq(i).text())

    game_arr = []
    game_collect = header.find('.gpugames_header_games')
    for i in range(0, game_collect.length):
        temp = []
        img_filename = os.path.split(game_collect.eq(i).find('img')[0].attrib['src'])[1]
        img = 'http://www.notebookcheck.net/typo3temp/_processed_/' + img_filename
        temp.append(game_collect.eq(i).text())
        temp.append(img)
        game_arr.append(temp)

    return game_arr, setting_arr

def gamemark_gpumark_processer(data, setting_arr):
    gupType = {'odd':1,'even':1,'desk_odd':1,'desk_even':1}
    gpu_arr = []

    if 'class' in data[0].attrib and data[0].attrib['class'] in gupType:
        specs = data.find('.specs')
        field_high = data.find('td')
        for i in range(specs.length-1):
            gpu_arr.append(specs.eq(i).text())

        for i in range(field_high.length-1):
            #field_high.eq(i).attr['class'] != 'gpugames_spacer'
            if (field_high.eq(i).attr['class'] is not None and (
            field_high.eq(i).attr['class'].startswith('gpugames_field') or
            field_high.eq(i).attr['class'] == 'specs')
            ):
                gpu_arr.append(field_high.eq(i).text())
    return gpu_arr


def gamemark_processer(table_name, gamemark_webpage):
    game_arr = []
    game_setting_num = []
    setting_arr = []

    gpus_arr = []
    gpus_arr_exchange = []

    data = file_reader(gamemark_webpage)
    pydata = pq(data)
    tr_collect = pydata.find('#sortierbare_tabelle tr')

    for i in range(0, tr_collect.length-1):
        if i == 0:
            continue
        elif i == 1:
            game_arr, setting_arr = gamemark_header_processer(tr_collect.eq(i-1), tr_collect.eq(i))
            insert_gamepic(game_arr)
        else:
            temp_arr = gamemark_gpumark_processer(tr_collect.eq(i), setting_arr)
            if len(temp_arr) == 0:
                continue
            gpus_arr.append(temp_arr)


    for each in setting_arr:
        game_setting_num.append(len(each))

    for each_gpu in gpus_arr:
        temp_arr = [[]]*(len(game_setting_num)+3)
        j = 3
        k = 0
        temp_arr[0] = each_gpu[0]
        temp_arr[1] = each_gpu[1]
        temp_arr[2] = each_gpu[2]
        for each in game_setting_num:
            i = 0
            temp = []
            while i < each:
                temp.append(each_gpu[k+3])
                i += 1
                k += 1
            temp_arr[j].append(temp)
            j += 1
        gpus_arr_exchange.append(temp_arr)

    for index, each in enumerate(gpus_arr_exchange):
        print each[2]#显卡型号
        gpuname = each[2]
        for game_index, game in enumerate(each[3]):
            print game_arr[game_index][0]#游戏名字
            for option_index, option in enumerate(game):
                    if len(option) > 0:
                        print gpuname, setting_arr[game_index][option_index]+':'+str(option)#游戏配置 + 帧数
                        dbctr.dbinserterGpuGameOptionFPS(table_name,
                                                         gpuname, game_arr[game_index][0],
                                                         setting_arr[game_index][option_index],
                                                         str(option))


cpu_processer('CpuMark',"output/source/cpupage.html")
cpu_processer('GpuMark',"output/source/gpupage.html")
gamemark_processer("GameMark", "output/source/gamemark.html")
