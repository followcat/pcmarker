__author__ = 'followcat'

import urllib2

import re
import MySQLdb
import MySQLdb.cursors

host = ''
user = ''
passwd = ''
db = ''
port = 3306

def init_dbset():
    global host,user,passwd,db,port
    fp_handle = open('../rssdb.set', 'r')
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



def checkGameMarkPic():
    try:
        conn = MySQLdb.connect(host = host,user = user, passwd = passwd,db = db,charset = 'utf8')
        cur = conn.cursor()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return
    cur.execute("SELECT * FROM GamePic;")
    rs=cur.fetchall()
    for each in rs:
        print each[1],each[2]

    cur.close()
    conn.close()

def search(word):
    url='http://www.google.com.hk/search?tbs=isz%3Am%2Ciar%3At&tbm=isch&sa=1&q='+word+'&biw=1745&bih=835'
    req=urllib2.Request(url)
    req.add_header("User-Agent",'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.2; .NET CLR 1.1.4322)')
    opener=urllib2.build_opener()
    text=opener.open(req).read()

    result = re.findall(r"/imgres\?imgurl=http://[a-zA-Z0-9./]+.jpg", text)
    for each in result:
        print each.replace('/imgres?imgurl=','')


print search("Company+of+Heroes+2+2013")

#init_dbset()
#checkGameMarkPic()