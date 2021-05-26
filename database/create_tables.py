import psycopg2


def create_tables(cur, conn):
	try:
		create = open('database/create.sql', 'r')
		tables = create.read().split(';')

		for table in tables:
			cur.execute(table)

		cur.close()
		conn.commit()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
