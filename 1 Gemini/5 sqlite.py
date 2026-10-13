import sqlite3
connection=sqlite3.connect("student.db")

cursor=connection.cursor()

table_info="""
Create table STUDENT(NAME VARCHAR(25),CLASS VARCHAR(25),SECTION VARCHAR(25),MARKS INT);

"""
cursor.execute(table_info)

cursor.execute('''Insert Into STUDENT values('Dr Ganapathi','Data Science','A',100)''')
cursor.execute('''Insert Into STUDENT values('AK garu','Data Science','B',98)''')
cursor.execute('''Insert Into STUDENT values('VCube','Data Analytics','A',100)''')
cursor.execute('''Insert Into STUDENT values('Sai','DEVOPS','A',50)''')

cursor.execute('''Insert Into STUDENT values('Srinu','Python','A',60)''')

print("The isnerted records are")
data=cursor.execute('''Select * from STUDENT''')

for row in data:
    print(row)

connection.commit()
connection.close()
