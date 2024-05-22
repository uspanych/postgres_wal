import os
import time
import psycopg2
import subprocess
from psycopg2 import OperationalError
import requests
"""Скрипт проверяет доступность реплики, в случае отсутсвия соединения от хоста, создается файл триггер"""


class Agent:
    def __init__(
        self,
        host: str,
        port: str,
        dbname: str,
        user: str,
        password: str,
        role: str,
        table: str,
    ):
        self.host = host
        self.port = port
        self.dbname = dbname
        self.user = user
        self.password = password
        self.role = role
        self.table = table

    def init_table(self):
        try:
            conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                port=self.port,
                host=self.host
            )

            cur = conn.cursor()
            cur.execute(
                "CREATE TABLE test (id int)"
            )
            conn.commit()
            cur.close()
            conn.close()
        except:
            print('Ошибка создания')

    def check_is_alive(
        self
    ) -> bool:

        if self.role == 'Slave':
            try:
                conn = psycopg2.connect(
                    dbname=self.dbname,
                    user=self.user,
                    password=self.password,
                    port=self.port,
                    host=self.host
                )

                cur = conn.cursor()
                cur.execute(
                    "SELECT * FROM test"
                )
                conn.commit()
                cur.close()
                conn.close()
                print('Master is alive')

                return True

            except OperationalError:
                print('Agent check - Master is dead...')

                response = requests.get('http://pg_arbiter:8000/check/pg-master')

                if response:
                    master_status = response.json()

                    if master_status.get('Master') == 'Dead':
                        print('Arbiter check - Master is dead...')

                        print('Promoting...')

                        subprocess.run(["touch",  "/tmp/promote_me_to_master"])

                        return False

if __name__ == "__main__":

    role = os.environ['ROLE']

    if role == 'Slave':
        agent = Agent(
            host=os.environ['MASTER_HOST'],
            port='5432',
            dbname=os.environ['POSTGRES_DB'],
            user=os.environ['POSTGRES_USER'],
            password=os.environ['POSTGRES_PASSWORD'],
            role=role,
            table='test_table',
        )
        agent.init_table()
        status = True

        while status:
            status = agent.check_is_alive()
            time.sleep(10)

