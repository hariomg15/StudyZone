import os
import psycopg2
from dotenv import load_dotenv

load_dotenv('.env')
url = os.environ.get('DATABASE_URL')
print('DATABASE_URL', url)
conn = psycopg2.connect(url)
cur = conn.cursor()
cur.execute("SELECT tablename FROM pg_tables WHERE schemaname='public';")
print('tables=', [r[0] for r in cur.fetchall()])
cur.execute("SELECT * FROM information_schema.tables WHERE table_schema='public' AND table_name='alembic_version';")
print('alembic_version table=', cur.fetchall())
try:
    cur.execute('SELECT version_num FROM alembic_version')
    print('version_num', cur.fetchone())
except Exception as e:
    print('version_query_error', e)
cur.close()
conn.close()