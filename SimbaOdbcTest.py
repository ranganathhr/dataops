import os
import argparse
import pyodbc
import sys

parser = argparse.ArgumentParser(description='Driver Functionality Test Suite')
parser.add_argument('--catalog', help='Driver flag to set the catalog name')
parser.add_argument('--dbname', help='The dbname which contains the tpcds tables of the required scale in case of tpcds runs')
parser.add_argument('--host', help='hostname')
parser.add_argument('--port', help='port')
parser.add_argument('--ssl', action='store_true', help='SSL')
parser.add_argument('--cert', help='SSL cert path')
args = parser.parse_args()


def runbvt():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    bvt_workload = os.path.join(root_dir, 'workloads/bvt')
    odbc_logpath = os.path.join(root_dir, 'logs/odbc')
    result_path = os.path.join(root_dir, 'result/bvt')

    if 'linux' in sys.platform:
        driverpath = ''
    elif 'darwin' in sys.platform:
        driverpath = '/Library/simba/prestoodbc/lib/libprestoodbc_sbu.dylib'

    connection_string = 'DRIVER={{{driverpath}}};HOST={host};PORT={port};CATALOG={catalog};SCHEMA={dbname};LOGLEVEL=6;LOGPATH={driverlog};'.format(driverpath=driverpath, host=args.host, port=args.port, catalog=args.catalog, dbname=args.dbname, driverlog=odbc_logpath)
    if args.ssl:
        connection_string += 'SSL=1;'
        connection_string += 'TRUSTEDCERTS={cert}'.format(cert=args.cert)

    conn = pyodbc.connect(connection_string, autocommit=True)
    cursor = conn.cursor()
    wrt = open(result_path + '/bvtresult.out', 'a+')
    for file in os.listdir(bvt_workload):
        with open(file, 'r').read() as sql:
            try:
                cursor.execute(str(sql).replace(';', ''))
                wrt.write(file)
                for row in cursor.fetchall():
                    wrt.write(str(row))
                wrt.write('='*50)
            except pyodbc.Error as pye:
                print(pye)


if __name__ == "main":
    runbvt()
