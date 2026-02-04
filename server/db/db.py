import psycopg2
from psycopg2.extras import RealDictCursor

DB_CONFIG = {
    'dbname': 'intuitive_care',
    'user': 'postgres',
    'password': 'senhadb',
    'host': 'localhost',
    'port': '5432'
}

def execute_query(query: str, params: tuple = None, fetch_one: bool = False):
    conn = psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    cursor.execute(query, params)
    
    if fetch_one:
        result = cursor.fetchone()
    else:
        result = cursor.fetchall()
    
    conn.close()
    return result