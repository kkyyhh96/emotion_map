import psycopg2

#连接数据库
conn = psycopg2.connect(database="EmotionMap", user="postgres",
                        password="postgres", host="127.0.0.1", port="5432")
cur = conn.cursor()
#读取数据
cur.execute("SELECT * FROM photos")
data_1=cur.fetchone()
print(data_1)
data_2=cur.fetchmany(1)
print(data_2)
data_3=cur.fetchall()
print(data_3)
data_4=cur.fetchone()
print(data_4)
if data_4 is None:
    print(True)
#插入数据
cur.execute("INSERT INTO photos "
            "VALUES(18, '1', '2', '(3,2)', 1.0, "
            "'2014-6-6', False, False)")
conn.commit()
#修改数据
cur.execute("UPDATE photos "
            "SET url='10'"
            "WHERE id=6")
conn.commit()
#删除数据
cur.execute("DELETE FROM photos "
           "WHERE id=11")
conn.commit()
conn.close()