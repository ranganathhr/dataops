import mysql.connector
import argparse
import random
from faker import Faker
import os

parser = argparse.ArgumentParser()
parser.add_argument('--action')
parser.add_argument('--tablename')
parser.add_argument('--limit')
args = parser.parse_args()

fake = Faker()
dbconfig = {
    'user': 'admin',
    'password': 'qubole123',
    'host': 'quboledb.cttgevjppcjr.us-east-1.rds.amazonaws.com',
    'database': 'test',
    'raise_on_warnings': True
    }
conn = mysql.connector.connect(**dbconfig)

def create_table():
    sql = "CREATE TABLE " + args.tablename + ''' (
  `col1` int primary key, 
  `col2` int, 
  `col3` varchar(50), 
  `col4` float(20,10), 
  `col5` varchar(60), 
  `col6` date, 
  `col7` int)'''
    try:
        db = conn.cursor()
        db.execute(sql)
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)


def gen_random_data():
    file = open(str('/tmp/' + args.tablename + '.out'), 'a+')
    for i in range(1, int(args.limit)+1):
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
    command = "mysqlimport --local -u " + dbconfig.get('user') + " -p" + dbconfig.get('password') + " -h " + dbconfig.get('host') + " " + dbconfig.get('database') + " --fields-terminated-by='|' /tmp/" + args.tablename + ".out"
    os.system(str(command))
    file.close()


def random_insert():
    sql = "select max(col1) from " + args.tablename
    db = conn.cursor()
    db.execute(sql)
    results = db.fetchall()
    for row in results: max_seq = row[0]
    for i in range(1, int(args.limit)+1):
        col1 = max_seq + i
        col2 = random.randint(1111, 999999)
        col3 = fake.name()
        col4 = random.random()
        col5 = fake.text()[0:50]
        col6 = fake.date()
        col7 = fake.unix_time()
        sql = "insert into " + args.tablename + " values(" + str(col1) + "," + str(col2) + ",'" + col3 + "'," + str(col4) + ",'" + col5 + "','" + str(col6) + "'," + str(col7) + ")"
        db.execute(sql)
        conn.commit()


def random_update():
    sql = "select max(col1) from " + args.tablename
    db = conn.cursor()
    db.execute(sql)
    results = db.fetchall()
    for row in results: max_seq = row[0]
    for i in range(1, int(args.limit)+1):
        pk = random.randint(1, max_seq)
        col3 = fake.name()
        col6 = fake.date()
        sql = "update " + args.tablename + " set col3='" + str(col3) + "',col6='" + str(col6) + "' where col1=" + str(pk)
        db.execute(sql)
        conn.commit()


def random_delete():
    sql = "select max(col1) from " + args.tablename
    db = conn.cursor()
    db.execute(sql)
    results = db.fetchall()
    for row in results: max_seq = row[0]
    for i in range(1, int(args.limit)+1):
        pk = random.randint(1, max_seq)
        sql = "delete from " + args.tablename + " where col1=" + str(pk)
        db.execute(sql)
        conn.commit()


def main():
    if args.action == "generate":
        create_table()
        gen_random_data()
        os.system("rm /tmp/" + args.tablename + ".out")
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
