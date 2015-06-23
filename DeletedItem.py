import datetime
from peewee import *
import Lib
from MyDatabase import *

all_deleted_items = [];

class DeletedItem(Model):
    uID = IntegerField(unique=True);
    date = DateField();
    number = IntegerField();
    name = TextField();
    buySingleCost = DoubleField();
    buyTotalCost = DoubleField();
    receivedNum = IntegerField();
    sellSignlePrice = DoubleField();
    sellTotalPrice = DoubleField();
    receivedMoney = DoubleField();
    otherCost = DoubleField();
    basicProfit = DoubleField();
    otherProfit = DoubleField();
    totalProfit = DoubleField();
    buyer = CharField(max_length=120);
    buyPlace = CharField(max_length=120);
    payCards = TextField();
    ifDrop = BooleanField();

    class Meta:
        database = db;

def delete_all_deleted_items():
    for x in DeletedItem.select():
        x.delete_instance();

if __name__ == '__main__':
    pass;