import datetime, time

def str_to_date(str):
	res = time.strptime(str, '%Y-%m-%d');
	print(res)
	y, m, d = res[0:3]
	print(y, m, d)
	res = datetime.date(y, m, d)
	print (res)
	print( type(res) )
	return res;

str = "2015-06-17"
str_to_date(str)
