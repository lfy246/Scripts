#encoding='utf-8'
# date 2018/2/20
# author birthpla

import pymysql
import datetime

class save_data(object):
    def __init__(self,dbname):
        self.dbname = dbname
        self.conn = pymysql.connect(
            host = "localhost",
            port = 3306,
            user = "root",
            password = '',
            db = self.dbname,
            charset = 'utf8'
        )
        self.cursor = self.conn.cursor()#游标

    def create_table(self,tbname):
        sql = '''CREATE TABLE  `{tbname}` (
            {reg_no} varchar(100) primary key,
            {com_name}  varchar(300),
            {yyzz} varchar(3000),
            {base_info} varchar(3000),
            {dwcz} varchar(3000),
            {gdcz} varchar(3000)
            )'''

        try:
            self.cursor.execute(sql.format(tbname = tbname,reg_no = "reg_no",com_name = "com_name",
                                            yyzz = "yyzz",base_info = "base_info",dwcz = "dwcz",gdcz = "gdcz"))
        except Exception as e:
            print("创建表格失败......原因：",e)
        else:
            self.conn.commit()
            print("创建{}成功!".format(tbname))


    def insert_data(self,data,tbname):
        sql = '''INSERT INTO `{table_name}` VALUES('{reg_no}','{com_name}','{yyzz}',
        '{base_info}','{dwcz}','{gdcz}')'''

        try:
            self.cursor.execute(sql.format(table_name = tbname,reg_no = data["reg_no"],com_name = data["com_name"],
                                           yyzz = data["yyzz"],base_info = data["base_info"],dwcz = data["dwcz"],gdcz = data["gdcz"]))
        except Exception as e :
            self.conn.rollback()#回滚
            print("插入该组数据失败：",e)
        else:
            self.conn.commit()
            print("插入一条数据成功！")

    def get_hadcom(self,tbname):          #获取已爬取公司名称
        # sql = """ SELECT
        #         *
        #     FROM
        #         `{}`
        #     WHERE
        #
        #     )  """.format(tbname)
        sql = "SELECT com_name FROM esta "
        self.cursor.execute(sql)
        result = []
        result_set = self.cursor.fetchall()
        for name in result_set:
            result.append(name[0])
        return result



    def close_all(self):
        self.cursor.close()
        self.conn.close()




if __name__ == '__main__':
    data = {"reg_no":"java1","com_name":"3","yyzz":"中文","dwcz":"无","base_info":"3","gdcz":"4"}
    test = save_data("company")
    test.insert_data(data,'esta')
    print(test.get_hadcom('esta'))
    test.close_all()