import os
import argparse
import pyodbc
import sys


def runbvt():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    bvt_workload = os.path.join(root_dir, 'workloads/bvt')
    odbc_logpath = os.path.join(root_dir, 'logs/odbc')
    result_path = os.path.join(root_dir, 'result/bvt')

    if 'linux' in sys.platform:
        driverpath = '/opt/simba/prestoodbc/lib/64/libprestoodbc_sb64.so'
    elif 'darwin' in sys.platform:
        driverpath = '/Library/simba/prestoodbc/lib/libprestoodbc_sbu.dylib'

    connection_string = 'DRIVER={{{driverpath}}};HOST={host};CATALOG={catalog};SCHEMA={dbname};TimeZoneID={timezone};LOGLEVEL=6;LOGPATH={driverlog};'.format(driverpath=driverpath, host=args.host, catalog=args.catalog, dbname=args.dbname, timezone='UCT', driverlog=odbc_logpath)
    if args.ssl:
        connection_string += 'PORT=8443;'
        connection_string += 'SSL=1;'
        connection_string += 'TRUSTEDCERTS={cert};'.format(cert=args.cert)
    else:
        connection_string += 'PORT=8080;'

    conn = pyodbc.connect(connection_string, autocommit=True)
    cursor = conn.cursor()
    wrt = open(result_path + '/bvtresult.out', 'w+')
    for file in os.listdir(bvt_workload):
        with open(bvt_workload + "/" + file, 'r') as f:
            try:
                sql = f.read()
                cursor.execute(str(sql).replace(';', ''))
                wrt.write(file + '\n')
                for row in cursor.fetchall():
                    wrt.write(str(row) + '\n')
                wrt.write('='*50 + '\n')
            except pyodbc.Error as pye:
                print(pye)


parser = argparse.ArgumentParser(description='Driver Functionality Test Suite')
parser.add_argument('--catalog', help='Driver flag to set the catalog name')
parser.add_argument('--dbname', help='The dbname which contains the tpcds tables of the required scale in case of tpcds runs')
parser.add_argument('--host', help='hostname')
parser.add_argument('--ssl', action='store_true', help='SSL')
parser.add_argument('--cert', help='SSL cert path')
args = parser.parse_args()

runbvt()
