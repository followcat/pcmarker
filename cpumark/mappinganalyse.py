# -*- coding: UTF-8 -*-
from __future__ import division

from cpumark.fsdbmctr import gpudb, markdb
from cpumark.fsdbmctr import dbinserterGameMarkMapping



gpumark_dict = {}
gpugame_dict = {}
ans_dict = {}


for model, data in gpudb.iteritems():
    gpumark_dict[model] = {}
    gpumark_dict[model]['lower'] = model.lower()
    gpumark_dict[model]['mark'] = data['mark']


for model in markdb.keys():
    gpugame_dict[model] ={}
    gpugame_dict[model]['lower'] = model.lower().replace('nvidia ','').replace('amd ','')

i = 0
for game_gpu in gpugame_dict:
    for gpu in gpumark_dict:
        if gpugame_dict[game_gpu]['lower'] == gpumark_dict[gpu]['lower']:
            ans_dict[gpu] = {}
            ans_dict[gpu]['match'] = game_gpu
            ans_dict[gpu]['mult'] = 1.0
            i += 1

for each in ans_dict:
    ans_dict[each]['mark'] = gpumark_dict[each]['mark']

ans_middle = {}
for each in ans_dict:
    ans_middle[each] = ans_dict[each]['mark']

ans_middle = sorted(ans_middle.iteritems(), key=lambda d:d[1],reverse = True )

add_dict = {}

print len(gpumark_dict)
print len(ans_dict)
i = 0
for each in gpumark_dict:
    if each not in ans_dict:
        temp = {}
        i += 1
        '''
        for game_each in gpugame_dict:
            diff = difflib.Differ().compare(each,game_each)
            cmp_list = list(diff)
            counter = 0
            for result in cmp_list:
                if result[0] != ' ':
                    counter += 1
            temp[game_each] = counter/len(cmp_list)
        temp_list = sorted(temp.iteritems(), key=lambda d:d[1], reverse = False )'''
        print each
        for index,middle in enumerate(ans_middle):
            if gpumark_dict[each]['mark'] > middle[1]:
                print gpumark_dict[each]['mark']
                print middle[1]
                add_dict[each] = {}
                add_dict[each]['match'] = ans_dict[middle[0]]['match']
                add_dict[each]['mult'] = gpumark_dict[each]['mark']/gpumark_dict[middle[0]]['mark']
                break
            if index == len(ans_middle)-1:
                print gpumark_dict[each]['mark']
                print middle[1]
                add_dict[each] = {}
                add_dict[each]['match'] = ans_dict[middle[0]]['match']
                add_dict[each]['mult'] = gpumark_dict[each]['mark']/gpumark_dict[middle[0]]['mark']
print i
print len(add_dict)

for each in add_dict:
    dbinserterGameMarkMapping(each, add_dict[each]['match'], add_dict[each]['mult'])
    print each
    print add_dict[each]
    print gpumark_dict[each]['mark']


for each in ans_dict:
    dbinserterGameMarkMapping(each, ans_dict[each]['match'], ans_dict[each]['mult'])
    print each
    print ans_dict[each]
    print gpumark_dict[each]['mark']
