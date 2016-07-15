'/GetHardList',methods=['GET']
该接口用于获取硬件列表
参数：
    『table:"CpuMark"或"GpuMark"
    该参数为获取哪一硬件列表
    』
    『nums:int
    该参数为获取列表行数，0时为全表获取』



'/GetOneData',methods=['GET']
该接口用于某一硬件数据
参数：
    『table:"CpuMark"或"GpuMark"
    该参数指定需要查询硬件处于哪一硬件列表』
    『hardname:str
    该参数为所需查询硬件型号』



'/ProductSearch',methods=['GET']
该接口用于某一硬件在各购物网下价格
参数：
    『method：str
    该参数为调用哪一查询api接口』
    『fields：str
    该参数为该接口所需要获取的参数，各参数间用','连接』
    『fields_dict：js字典数据的字符串形态
    该参数由js字典数据组成，其内容由fields指定的需求决定』



'/GetNameList',methods=['GET']
该接口用于全名称获取
提示：
    该ajax调用例子请参看static/ProductSearchTest.html DEMO



'/GetGpuFps',methods=['GET']
该接口用于获取某张显卡的相关游戏帧数
参数：
    『gpuname：str
    该参数为查询Gpu的名字』
返回:
    {'map':map_gpu,'mult':mult,'fps':[]}
    json,map为对应帧数表的Gpu名字,mult如果不是1.0则是查询GPU对应map中GPU的倍率，fps是数组，里面放了各个游戏不同配置下的帧数，先请求获得帧数后再根据游戏名字获取游戏图片



'/GetGamePic',methods=['GET']
该接口用于获取某个游戏的缩略图的url链接
参数：
    『gamename：str
    该参数为查询Game的名字』
返回:
    返回Game对应缩略图的link


