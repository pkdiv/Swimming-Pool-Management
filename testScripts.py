import psycopg2
import psycopg2.extras

# conn = psycopg2.connect(
#         host="localhost",
#         database="swimming",
#         user='flask',
#         password='password')

# with open('testUser.csv', 'r') as file:
#     print(file.readline())

# cur = conn.cursor()
# cur.execute('''INSERT INTO users (name,roleid) VALUES (%s,%s) RETURNING user_id''', (name,3))
# result = cur.fetchone()
# cur.execute('''INSERT INTO login (user_id, email, password) VALUES (%s,%s,%s) RETURNING user_id''', (result[0], email,sha256_crypt.encrypt(password)))
# conn.commit()
# cur.close()