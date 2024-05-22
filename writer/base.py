import random
import time
import logging
import psycopg2
from concurrent.futures import ThreadPoolExecutor

def create_table():
    conn = psycopg2.connect(
        dbname='benchmark',
        user='postgres',
        password='postgres',
        host='localhost',
        port='5432'
    )

    cur = conn.cursor()

    cur.execute(
        "CREATE TABLE test(id int)"
    )

    conn.commit()
    cur.close()
    conn.close()


def insert_data():

    conn_master = psycopg2.connect(
        dbname='benchmark',
        user='postgres',
        password='postgres',
        host='localhost',
        port='5432'
    )

    cur_master = conn_master.cursor()
    conn_slave = psycopg2.connect(
        dbname='benchmark',
        user='postgres',
        password='postgres',
        host='localhost',
        port='5433'
    )

    cur_slave = conn_slave.cursor()

    def task(
        cur_master,
        cur_slave,
        i,
    ):
        time.sleep(random.choice([1, 2, 3]))

        try:
            cur_master.execute(
                "INSERT INTO test VALUES (%s)",
                (i,)
            )
            conn_master.commit()
            logging.warning(f'Записалось значение под номером -  {i}')
        except psycopg2.OperationalError:
            conn_master.rollback()
            cur_slave.execute(
                "INSERT INTO test VALUES (%s)",
                (i,)
            )
            conn_slave.commit()
            logging.warning(f'Записалось значение под номером -  {i}')

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(task, cur_master, cur_slave, i) for i in range(500000)]
        [future.result() for future in futures]
    cur_master.close()
    conn_master.close()

    cur_slave.close()
    conn_master.close()


def select_value():
    conn = psycopg2.connect(
        dbname='benchmark',
        user='postgres',
        password='postgres',
        host='localhost',
        port='5432'
    )

    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM test"
    )

    print(cur.fetchall())

    conn.commit()
    cur.close()
    conn.close()


if __name__ == '__main__':
    try:
        create_table()
    except:
        insert_data()
