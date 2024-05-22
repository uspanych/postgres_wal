from fastapi import FastAPI
import psycopg2
from psycopg2 import OperationalError
import os

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get('/check/{host_ip}')
def check_host(host_ip: str):
    try:
        conn = psycopg2.connect(
            dbname=os.environ['POSTGRES_DB'],
            user=os.environ['POSTGRES_USER'],
            password=os.environ['POSTGRES_PASSWORD'],
            port=5432,
            host=host_ip
        )

        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM test"
        )
        conn.commit()
        cur.close()
        conn.close()

        return {"Master": "Alive"}

    except OperationalError:
        return {"Master": "Dead"}
