import mysql.connector
import argparse
import random
from faker import Faker
import os

fake = Faker()

parser = argparse.ArgumentParser()
parser.add_argument('--action')
parser.add_argument('--tablename')
parser.add_argument('--limit')
args = parser.parse_args()

dbconfig = {
  'user': 'myuser',
  'password': 'mypassword',
  'host': 'myhost',
  'database': 'testdb',
  'raise_on_warnings': True
}


db = mysql.connector.connect(**dbconfig).cursor()


def create_table():
    sql = "CREATE TABLE " + args.tablename + ''' (
  `col1` int primary key, 
  `col2` int, 
  `col3` varchar(20), 
  `col4` float(20,10), 
  `col5` varchar(50), 
  `col6` date, 
  `col7` int)'''
    try:
        db.execute(sql)
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)


def gen_random_data():
    file = open(str('/tmp/' + args.tablename + '.out'), 'a+')
    for i in range(1, args.limit):
        col1 = i
        col2 = random.randint(1111, 999999)
        col3 = fake.name()
        col4 = random.random()
        col5 = fake.text()[0:50]
        col6 = fake.date()
        col7 = fake.unix_time()
        row_list = [str(col1), str(col2), str(col3), str(col4), str(col5), str(col6), str(col7)]
        row = "|".join(row_list)
        file.write(row + os.linesep)
    command = f"mysqlimport --local -u {dbconfig.get('user')} -p{dbconfig.get('password')} -h {dbconfig.get('host')} {dbconfig.get('database')} --fields-terminated-by='|' /tmp/{args.tablename}"
    os.system(command)
    file.close()
    print(f"Created table: {dbconfig.get('database')}.{args.tablename} with {args.limit} records")


def random_insert():
    sql = f"select max(col1) from {args.tablename}"
    db.execute(sql)
    results = db.fetchall()
    for row in results: max_seq = row[0]
    for i in range(1, args.limit):
        col1 = max_seq + i
        col2 = random.randint(1111, 999999)
        col3 = fake.name()
        col4 = random.random()
        col5 = fake.text()[0:50]
        col6 = fake.date()
        col7 = fake.unix_time()
        sql = f"insert into {args.tablename} values({col1}, {col2}, {col3}, {col4}, {col5}, {col6}, {col7})"
        db.execute(sql)
    print(f"Inserted new {args.limit} records to the table {dbconfig.get('database')}.{args.tablename}")


def random_update():
    sql = f"select max(col1) from {args.tablename}"
    db.execute(sql)
    results = db.fetchall()
    for row in results: max_seq = row[0]
    for i in range(1, args.limit):
        pk = random.randint(1, max_seq)
        col3 = fake.name()
        col6 = fake.date()
        sql = f"update {args.tablename} set col3={col3},col6={col6} where col1={pk}"
        db.execute(sql)
    print(f"Updated random {args.limit} records in the table {dbconfig.get('database')}.{args.tablename}")


def random_delete():
    sql = f"select max(col1) from {args.tablename}"
    db.execute(sql)
    results = db.fetchall()
    for row in results: max_seq = row[0]
    for i in range(1, args.limit):
        pk = random.randint(1, max_seq)
        sql = f"delete from {args.tablename} where col1={pk}"
        db.execute(sql)
    print(f"Deleted random {args.limit} records from the table {dbconfig.get('database')}.{args.tablename}")


def main():
    if args.action == "generate":
        create_table()
        gen_random_data()
    elif args.action == "insert":
        random_insert()
    elif args.action == "update":
        random_update()
    elif args.action == "delete":
        random_delete()
    else:
        print("Invalid action! only 'generate', 'insert', 'update' or 'delete' allowed")
        exit(1)


if __name__ == "__main__":
    main()
