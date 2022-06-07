import mysql.connector

connection = mysql.connector.connect(
    host = 'localhost',
    port = '3306',
    user = 'root',
    password = 'asd90614',
    database = 'myfin'
    )

cursor = connection.cursor()

#新增
#cursor.execute("INSERT INTO `user` VALUES(456, '小名' ,'asd123@gmail.com' ,'123456')")

cursor.execute("INSERT INTO `account` VALUES(69, '支出' ,'飲食' , '2022-06-07', '新台幣' ,456,2000)")

cursor.close()
connection.commit()
connection.close()