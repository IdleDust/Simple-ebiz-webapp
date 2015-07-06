import xlrd

from Item import *
import datetime, time
import Lib
import os


def process_file(file_name):
	# data = xlrd.open_workbook('06-15-eBiz.xlsx');
	data = xlrd.open_workbook(file_name);
	table = data.sheets()[0];
	nrow = table.nrows;
	for i in range(1,nrow):
		rowlist = table.row_values(i);
		# for j in range(len(rowlist)):
		# 	print ("{}:{}".format(j,rowlist[j]));
		dt = table.row_values(i)[0];
		a = Lib.toInt(dt[0:2]);
		b = Lib.toInt(dt[3:5]);
		c = Lib.toInt(dt[6:10]);
		date = datetime.date(c,a,b);
		number = table.row_values(i)[2];
		name = table.row_values(i)[1];
		buySingleCost = table.row_values(i)[3];
		receivedNum = table.row_values(i)[5];
		sellSignlePrice = table.row_values(i)[6];
		receivedMoney = table.row_values(i)[8];
		otherCost = table.row_values(i)[9];
		basicProfit = table.row_values(i)[10];
		otherProfit = table.row_values(i)[11];
		buyer = table.row_values(i)[13];
		buyPlace = table.row_values(i)[14];
		payCards = table.row_values(i)[16];
		ifDrop = table.row_values(i)[15];
		add_new_item(uID=0, date=date, name=name, number=number, buySingleCost=buySingleCost, \
		    receivedNum=receivedNum, sellSignlePrice=sellSignlePrice, receivedMoney=receivedMoney, \
		    otherCost=otherCost, basicProfit=basicProfit, otherProfit=otherProfit, buyer=buyer,\
		     buyPlace=buyPlace, payCards=payCards, ifDrop=ifDrop);

def process_all_files():
	info=os.getcwd();
	listfile=os.listdir(info);
	print(listfile);
	for i in range(len(listfile)):
		if listfile[i][-4:] == 'xlsx':
			print(listfile[i]);
			process_file(listfile[i]);


if __name__ == '__main__':
	process_all_files();
