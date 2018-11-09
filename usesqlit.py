import sqlite3

class MySql():
    def __init__(self,database):
        # 连接数据库
        self.database = database
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        cursor.execute('''create table if not exists urldata
                       (url CHAR primary key     not null ,
                        accessed BOOLEAN 
                        );''')
        conn.commit()
        conn.close()

    #保存url，且去掉重复url
    def url_save(self,url):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        for u in url:
            #将url设为主键重复插入时会报错，try用来规避重复插入。并且可以给其他进程发送信号
            try:
                cursor.execute("insert into {} (url,accessed)values (?,?)".format('urldata'),(u,0))
            except Exception:
                pass
        conn.commit()
        conn.close()

    def url_read(self):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        data = cursor.execute('select * from {}'.format('urldata'))
        conn.commit()
        print(data.fetchall())
        conn.close()

    #访问url函数，如果将一个url取出来访问，便将标志设置成TRUE
    def url_access(self):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        data = cursor.execute('select * from {} where accessed = {}'.format('urldata',0))
        urlmatrix = data.fetchall()
        conn.commit()
        conn.close()
        return urlmatrix

    def set_url_acce(self,url):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        cursor.execute('update {} set accessed = ? where url = ?'.format('urldata'),(1,url))
        conn.commit()
        conn.close()

# mysql = MySql('first.db')
# mysql.url_save('https://blog.csdn.net/shuishen520/article/details/83861996')
# mysql.url_access()
# mysql.url_read()