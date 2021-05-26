import re
from datetime import datetime, timedelta
import discord
import psycopg2
from database.config import config
import schedule
import time


async def save(test, msg):
	try:
		subject = test.split(' ')[1]
	except (Exception, psycopg2.DatabaseError) as error:
		await msg.channel.send("Subject can't be empty")
		return

	values = re.findall('\[(.*?)\]', test)
	if len(values) == 0:
		await msg.channel.send("Date can't be empty")
		return

	date = None
	try:
		date = datetime.strptime(values[0], '%m/%d/%y %H:%M:%S')
	except (Exception, psycopg2.DatabaseError) as error:
		await msg.channel.send("Violate date format - [month/day/year hour:minute:second]")
		return

	note = None
	if len(values) == 1:
		note = values[1]

	insert_test({'subject': subject, 'date': str(date), 'note': note, 'teacher': None})
	return date.day - date.now().day


async def send_test(content, channel):
	description = 'Test will be tomorrow'
	if content['note'] is not None:
		description = content['note']

	embed = discord.Embed(
		title='Test z ' + content['subject'] + ' - ' + str(content['date']),
		description=description,
		color=0xFF5733
	)
	await channel.send(embed=embed)


def insert_test(values):
	conn = None
	try:
		params = config()
		conn = psycopg2.connect(**params)
		cur = conn.cursor()
		cur.execute(
			""" INSERT INTO tests (subject, "date", note, teacher) VALUES (%s, %s, %s, %s)""",
			(values['subject'], values['date'], values['note'], values['teacher'])
		)
		conn.commit()
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()
			print('Database connection closed.')


async def get_tests(channel):
	conn = None
	try:
		params = config()
		conn = psycopg2.connect(**params)
		cur = conn.cursor()

		tomorrow_date = datetime(2020, 2, 20)
		tomorrow_date += timedelta(days=1)
		tomorrow_date = str(tomorrow_date)
		tomorrow_date = tomorrow_date.replace("00", "")
		tomorrow_date = tomorrow_date.replace(":", "")
		tomorrow_date = tomorrow_date.replace(" ", "")

		cur.execute("SELECT * FROM tests WHERE date >= '" + tomorrow_date + "'::timestamp")
		rows = cur.fetchall()
		print("The number of parts: ", cur.rowcount)
		for row in rows:
			await send_test({'subject': row[1], 'date': row[2], 'teacher': row[3], 'note': row[4]}, channel)

		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()


def schedule_test_notifications():
	schedule.every(10).minutes.do(get_tests)
	while True:
		schedule.run_pending()
		time.sleep(1)
