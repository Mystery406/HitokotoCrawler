import time
import urllib.request
import json
import pymysql


def request_hikotoko_to_db(x):
    html = urllib.request.urlopen('https://v1.hitokoto.cn/')
    hjson = json.loads(html.read())
    is_new = check_hikotoko(hjson, x)
    if is_new:
        save_to_db(hjson)
    time.sleep(0.1)


def check_hikotoko(hjson, x):
    content = hjson['hitokoto']
    source = hjson['from']
    sql = "select * from hitokoto where content=%s and source=%s"
    cursor.execute(sql, (content, source))
    if cursor.fetchone():
        print("%s,这条已存在" % x)
        return False
    else:
        print("%s,这条是新的" % x)
        return True


def save_to_db(hjson):
    content = hjson['hitokoto']
    type_ = hjson['type']
    source = hjson['from']
    creator = hjson['creator']
    created_at = hjson['created_at']
    sql = "insert into hitokoto(id,content,type,source,creator,created_at) values (0,%s,%s,%s,%s,%s)"
    cursor.execute(sql, (content, type_, source, creator, created_at))
    conn.commit()


print("Crawler Start")
conn = pymysql.connect("localhost", "root", "123456", "oneforall")
cursor = conn.cursor()
for x in range(1, 1000):
    request_hikotoko_to_db(x)
conn.close()
print("Crawler End")
