import psycopg2
import os

def connection():
    return psycopg2.connect(os.getenv("DATABASE_URL"))
