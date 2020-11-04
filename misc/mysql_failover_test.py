import pymysql.cursors
import time
import os

# Init
aurora = 'xxx.rds.amazonaws.com'
proxy = 'xxx.rds.amazonaws.com'
user = os.getenv('user')  # from OS environment variable $user
password = os.getenv('password')  # from OS environment variable $password

# Point the endpoint directly to aurora or through proxy
endpoint = proxy


def connect(endpoint):
    # Create connection
    connection = pymysql.connect(host=endpoint,
                                 user=user,
                                 password=password,
                                 db='HR',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection


def query():
    # Cursor
    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT COUNT(*) as total_employees, NOW() as datetime FROM EMPLOYEES"
        cursor.execute(sql)
        result = cursor.fetchone()
        print(f'There are {result["total_employees"]} employees at {result["datetime"]}')


while True:
    # Execute the query every 1s until killed
    print(f'Connecting to {endpoint}')
    connection = connect(endpoint)
    query()
    print('Closing connection')
    connection.close()
    time.sleep(1)
