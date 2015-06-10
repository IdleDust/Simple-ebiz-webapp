
import datetime

def get_current_date():
	x = datetime.datetime.now();
	return datetime.date(x.year, x.month, x.day);

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