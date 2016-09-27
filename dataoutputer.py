import MySQLdb
class DataOutputer:

    def __init__(self):
        self.datas = []
    def clear_data(self):
        self.datas = []
    def collect_data(self, data):
        if data is None:
            return
        self.datas.append(data)

    def output_html(self,type):
        filename = 'tangshi.html'
        if type==1:
            filename = 'songsan.html'
        fout = open(filename, 'w')
        fout.write("<html>\n")
        fout.write("<head>\n")
        fout.write("<meta charset = \"UTF-8\" >\n")
        fout.write("</head>\n")
        fout.write("<body>\n")
        fout.write("<table>\n")
        for data in self.datas:
            fout.write("<tr>\n")
            fout.write("<td>%s</td>\n" % data['title'].encode('utf-8'))
            fout.write("<td>%s</td>\n" % data['author'].encode('utf-8'))
            fout.write("<td>%s</td>\n" % data['content'].encode('utf-8'))
            fout.write("</tr>\n")
        fout.write("</table>\n")
        fout.write("</body>\n")
        fout.write("</html>\n")
        fout.close()
        return
    def output_db(self,type):
        conn = MySQLdb.connect(
            host = 'localhost',
            user = 'root',
            passwd = '123456',
            port = 3306,
            db = 'rainbellpoem',
            charset = 'utf8'
        )
        cursor = conn.cursor()
        if type==0:
            tablename = 'tangshi'
        elif type==1:
            tablename = 'songsan'
        sql_create = 'create table if not exists %s(title VARCHAR(100),author VARCHAR(50),content TEXT )' % tablename
        cursor.execute(sql_create)
        sql_delete = 'delete from %s' % tablename
        cursor.execute(sql_delete)
        conn.commit()
        for data in self.datas:
            sql_insert = 'insert into %s(title,author,content) VALUES(\'%s\',\'%s\',\'%s\')'
            sql_insert %= (tablename,data['title'],data['author'],data['content'])
            cursor.execute(sql_insert)
        conn.commit()
        cursor.close()
        conn.close()