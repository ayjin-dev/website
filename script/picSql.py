import pymysql
import os
import datetime

def PicList():
    path ='./static'
    picList = []
    print(os.listdir(path))
    for root,dirs,files in os.walk(path):
        for file in files:
            oripath = os.path.join(root,file)
            or1 = oripath.replace('\\','/')
            newpath = or1[1:]
            title = newpath.split('/')[-1].split('.')[0]
            picmsg = {
                'title':title,
                'path':newpath
            }
            picList.append(picmsg)
    return picList

def addPic(picList):
    # 连接数据库
    connect = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='xxx',
        db='website',
        charset='utf8'
    )
    # 获取游标
    cursor = connect.cursor()

    # 插入数据
    sql = "INSERT INTO servermanager_picmanage (title, path) VALUES ( '%s', '%s')"
    for picmsg in picList:
        try:
            data = (picmsg['title'], picmsg['path'])
            cursor.execute(sql % data)
            connect.commit()
        except Exception as e:
            print(e)
    print('成功插入', cursor.rowcount, '条数据')
    # 关闭连接
    cursor.close()
    connect.close()
if __name__ == '__main__':
    picList = PicList()
    print(picList)