
import datetime, time
import math, random

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

def toDecimal(x):
	try:
		return round(x,1);
	except:
		return 0;

def get_cur_time_stamp():
	x = toInt(math.ceil(time.time()*100));
	left = str(x)[-5:];
	right = str(get_random_number());
	res = toInt(left + right);
	return res;

def get_random_number():
	return random.randint(10000, 99999);


def get_unique_ID():
	return get_cur_time_stamp();

def max_common_substr_len(x, y):
	lx = len(x);
	ly = len(y);
	if lx == 0 or ly == 0:
		return 0;
	c = [[0 for j in range(ly+2)] for i in range(lx+2)];
	for i in range(1,lx+1):
		for j in range(1,ly+1):
			if x[i-1] == y[j-1]:
			    c[i][j] = c[i-1][j-1] + 1;
			else:
			    c[i][j] = max(c[i-1][j], c[i][j-1]);
	return c[lx][ly];






