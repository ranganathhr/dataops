Random Data generator
==============================

Prerequisites
-------------
* Install python
* pip install mysql-connector-python
* pip install argparse
* pip install Faker
* Install MySQL client (Amazon Linux):
    sudo yum update
    sudo yum install mysql


How to run
-------------
Synatax:

* To create a table and generate random data. limit indicates the number of records to be generated

Schema used:
col1 int primary key, col2 int, col3 varchar(20), col4 float(20,10), col5 varchar(50), col6 date, col7 int

python dataops.py --generate --tablename=test --limit 10000


* To randomly update records. This updates 100 random records

python dataops.py --update --tablename=test --limit 100


* To randomly Insert records. This Inserts 100 new records

python dataops.py --insert --tablename=test --limit 100


* To randomly Delete records. This deletes 100 random records

python dataops.py --delete --tablename=test --limit 100