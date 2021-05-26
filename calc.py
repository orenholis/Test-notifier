import re


def add(example):
	count = 0
	numbers = example.split('+')
	for num in numbers:
		if re.search("[0-9]+", num):
			count += int(num)
	return str(count)


def multiple(example):
	count = 0
	numbers = example.split('*')
	for num in numbers:
		print(num)
		if re.search("[0-9]+", num):
			count *= int(num)
	return str(count)
