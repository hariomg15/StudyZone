import os
import psycopg2
from dotenv import load_dotenv

load_dotenv('.env')
conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS enrollments, notes, lectures, sections, courses, users CASCADE;")
cur.execute("DROP TYPE IF EXISTS userrole;")
conn.commit()
cur.close()
conn.close()
print("DB cleanup done")