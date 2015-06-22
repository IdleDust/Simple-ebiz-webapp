
import datetime, time

def get_current_date():
	x = datetime.datetime.now();
	return datetime.date(x.year, x.month, x.day);

def str_to_date(str):
	res = time.strptime(str, '%Y-%m-%d');
	y, m, d = res[0:3]
	res = datetime.date(y, m, d)
	return res;

def toInt(x):
	try:
		return int(x);
	except ValueError:
		return 0;

def toFloat(x):
	try:
		return float(x);
	except ValueError:
		return 0;

def get_cur_time_stamp():
	return toInt(time.time()*100);

def get_unique_ID():
	return get_cur_time_stamp();

	
