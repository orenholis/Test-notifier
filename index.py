from datetime import datetime

import discord
import test_store
import calc
import json
import helpers


client = discord.Client()

@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))
	send_message.start()

@client.event
async def on_message(msg):
	if msg.author == client.user:
		return

	if msg.content.startswith('!'):
		if msg.content.startswith('!add'):
			result = calc.add(msg.content.replace('!add', ''))
			await msg.channel.send('Result is ' + result)

		if msg.content.startswith('!test'):
			notification_date = await test_store.save(msg.content.replace('!test', ''), msg)
			await msg.channel.send("Test was saved notification will be shown in " + str(notification_date) + " days")

		if msg.content.startswith('!channel'):
			f = open('config.json', "r")
			data = json.loads(f.read())
			admin = data.get('admin')
			if admin is None:
				await msg.channel.send("Set admin using command !admin")
				return
			elif admin.index(msg.author.id) < 0:
				await msg.channel.send("You don't have right to set a channel ask admin")
				return

			data['notification_channel'] = msg.channel.id
			with open("config.json", "w") as write_file:
				json.dump(data, write_file)
			msg.channel.send("Channel was set to sending notifications to tests")

		if msg.content.startswith('!help'):
			if msg.content.replace('!help ', '') == 'admin':
				await msg.channel.send(
					"First user who use this is admin of bot"
					"For adding more admins must user who wants to be admin "
					"must type !pingid which will give him in dm his user id "
					"this will he send to main admin and main admin will type in dm"
					"!admin [user-id]"
				)
				return

			if msg.content.replace('!help ', '') == 'channel':
				await msg.channel.send(
					"You must set a channel where will be sent notifications to test"
				)
				return

			await msg.channel.send(
				"You can use command !test in format !test subject name [date of test] [note] \n" +
				"Date format - [month/day/year hour:minute:second] \n" +
				"Notification on test will be shows day before test at 7PM \n" +
				"Set an admin using !admin \n" +
				"Set a channel where will be notifications send using !channel \n"
			)

		if msg.content.startswith('!admin'):
			f = open('config.json', "r")
			data = json.loads(f.read())
			admin = data.get('admin')
			if admin is None:
				data['admin'] = [msg.author.id]
			elif data['admin'][0] == msg.author.id:
				data['admin'].append(int(msg.content.replace('!admin ', '')))
			else:
				msg.channel.send('You are not admin ask admin for adding')
			with open("config.json", "w") as write_file:
				json.dump(data, write_file)
			await msg.channel.send("You were set as admin")

		if msg.content.startswith('!pingid'):
			await msg.author.send('Your id is ' + str(msg.author.id))

		if msg.content.startswith('!features'):
			await msg.author.send(
					'Upcoming features: \n' +
					'1) google calendar events \n' +
					'2) checking valid subjects and converting them to normal\n' +
                    '3) adding names of teachers to notidication automaticaly\n' +
					'4) bot managing on web \n' +
					'5) updating and deleting test notifications'
          )


@tasks.loop(minutes=30.0)
async def send_message():
	if datetime.now().hour == 19:
		channel = client.get_channel(helpers.load_json_value('notification_channel'))
		await test_store.get_tests(channel)

token = helpers.load_json_value('token')
client.run(token)
test_store.schedule_test_notifications()
