__author__ = 'followcat'
import MySQLdb
import MySQLdb.cursors

host = ''
user = ''
passwd = ''
db = ''
port = 3306

def init_dbset():
    global host,user,passwd,db,port
    fp_handle = open('rssdb.set', 'r')
    lines = fp_handle.readlines()
    for line in lines:
        dataset = line.strip('\n').split(':')
        if 0 == len(dataset[1]):
            dataset[1] = ''
        if dataset[0] == 'host':
            host = dataset[1]
        if dataset[0] == 'user':
            user = dataset[1]
        if dataset[0] == 'passwd':
            passwd = dataset[1]
        if dataset[0] == 'db':
            db = dataset[1]
        if dataset[0] == 'port':
            port = int(dataset[1])

def init_db():
    #Link To DB
    try:
        conn = MySQLdb.connect(host = host,user = user, passwd = passwd,db = db,charset = 'utf8')
        cur = conn.cursor()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        if e.args[0] == 1049:
            #Create DB
            print "Create DB"
            try:
                conn = MySQLdb.connect(host = host,user = user, passwd = passwd,charset = 'utf8')
                cur = conn.cursor()
                cur.execute("CREATE DATABASE %s DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci"%(db))
                conn.commit()
                #Relink DB after
                conn=MySQLdb.connect(host = host,user = user, passwd = passwd,db = db,charset = 'utf8')
                cur=conn.cursor()
            except MySQLdb.Error,e:
                print "Mysql Error %d: %s" % (e.args[0], e.args[1])
                return

    #Create Table
    try:
        cur.execute("CREATE TABLE if not exists CpuMark \
        ("
                    "id int(11) NOT NULL auto_increment,"
                    "model varchar(64),"
                    "mark int,"
                    "rank int,"
                    "value text,"
                    "price text,"
                    "PRIMARY KEY  (id),"
                    "UNIQUE KEY update_or_insert (model)"
                    ")")
        conn.commit()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return

    try:
        cur.execute("CREATE TABLE if not exists GpuMark \
        ("
                    "id int(11) NOT NULL auto_increment,"
                    "model varchar(64),"
                    "mark int,"
                    "rank int,"
                    "value text,"
                    "price text,"
                    "PRIMARY KEY  (id),"
                    "UNIQUE KEY update_or_insert (model)"
                    ")")
        conn.commit()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return

    try:
        cur.execute("CREATE TABLE if not exists GamePic \
        ("
                    "id int(11) NOT NULL auto_increment,"
                    "game varchar(64),"
                    "link text default NULL,"
                    "PRIMARY KEY  (id),"
                    "UNIQUE KEY update_or_insert (game)"
                    ")")
        conn.commit()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return


    try:
        cur.execute("CREATE TABLE if not exists GpuGameMark \
        ("
                    "id int auto_increment,"
                    "Gpu varchar(64),"
                    "Game varchar(64),"
                    "Options varchar(64),"
                    "FPS text default NULL,"
                    "PRIMARY KEY  (id),"
                    "UNIQUE KEY update_or_insert (Gpu,Game,Options)"
                    ")")
        conn.commit()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return

    try:
        cur.execute("CREATE TABLE if not exists GameMarkMapping \
        ("
                    "id int auto_increment,"
                    "Gpu varchar(64),"
                    "Mapping varchar(64),"
                    "Mult float default NULL,"
                    "PRIMARY KEY  (id),"
                    "UNIQUE KEY update_or_insert (Gpu)"
                    ")")
        conn.commit()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return

    cur.close()
    conn.close()

def dbinserterCpuGpuMark(table,model,mark,rank,value,price):
    try:
        conn = MySQLdb.connect(host = host,user = user, passwd = passwd,db = db,charset = 'utf8')
        cur = conn.cursor()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return
    try:
        #str_exec = (r"INSERT INTO %s(model,mark,rank,value,price) SELECT '%s',%d,%d,'%s','%s' FROM dual  WHERE NOT EXISTS (SELECT * FROM %s WHERE %s.model = '%s')" %(table,model,mark,rank,value,price,table,table,model))
        str_exec = (r"INSERT INTO %s(model) values('%s') ON DUPLICATE KEY UPDATE mark='%d',rank=%d,value='%s',price='%s'"%(table,model,mark,rank,value,price))
        cur.execute(str_exec)
        conn.commit()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return
    cur.close()
    conn.close()


def dbinserterGameMarkPic(Game,url):
    try:
        conn = MySQLdb.connect(host = host,user = user, passwd = passwd,db = db,charset = 'utf8')
        cur = conn.cursor()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return
    try:
        str_exec = (r"INSERT INTO GamePic(game) values ('%s') ON DUPLICATE KEY UPDATE link='%s'"%(Game,url))
        cur.execute(str_exec)
        conn.commit()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return
    cur.close()
    conn.close()

def dbinserterGpuGameOptionFPS(Gpu,Game,Options,FPS):
    try:
        conn = MySQLdb.connect(host = host,user = user, passwd = passwd,db = db,charset = 'utf8')
        cur = conn.cursor()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return
    try:
        str_exec = (r"INSERT INTO GpuGameMark(Gpu,Game,Options) values ('%s','%s','%s') ON DUPLICATE KEY UPDATE FPS='%s'"%(Gpu,Game,Options,FPS))
        cur.execute(str_exec)
        conn.commit()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return
    cur.close()
    conn.close()

def dbinserterGameMarkMapping(Gpu,Mapping,Mult):
    try:
        conn = MySQLdb.connect(host = host,user = user, passwd = passwd,db = db,charset = 'utf8')
        cur = conn.cursor()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return
    try:
        str_exec = (r"INSERT INTO GameMarkMapping(Gpu) values ('%s') ON DUPLICATE KEY UPDATE Mapping='%s',Mult=%f"%(Gpu,Mapping,Mult))
        cur.execute(str_exec)
        conn.commit()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return
    cur.close()
    conn.close()

def trygamemark():
    try:
        conn = MySQLdb.connect(host = host,user = user, passwd = passwd,db = db,charset = 'utf8',cursorclass = MySQLdb.cursors.DictCursor)
        cur = conn.cursor()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return
    try:
        cur.execute('select Mapping,Mult from GameMarkMapping where Gpu = "GeForce G210"')
        result = cur.fetchone()
        print result
        map_gpu = result['Mapping']
        mult = result['Mult']
        print mult


        cur.execute('select * from GpuGameMark where Gpu = "'+map_gpu+'"')
        result = cur.fetchall()
        for each in result:
            print each

    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return
    cur.close()
    conn.close()

init_dbset()
init_db()
#trygamemark()
