import datetime
from peewee import *
import Lib
from MyDatabase import *
import DeletedItem

all_items = [];

class Item(Model):
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

    def print_item(self):
        info = dict()
        info['uID'] = self.uID
        info['date'] = self.date
        info['number'] = self.number
        info['name'] = self.name
        info['buySingleCost'] = self.buySingleCost
        info['buyTotalCost'] = self.buyTotalCost
        info['receivedNum'] = self.receivedNum
        info['sellSignlePrice'] = self.sellSignlePrice
        info['sellTotalPrice'] = self.sellTotalPrice
        info['receivedMoney'] = self.receivedMoney
        info['otherCost'] = self.otherCost
        info['basicProfit'] = self.basicProfit
        print(info.items())


def update_all_items():
    global all_items;
    all_items = Item.select();
    DeletedItem.all_deleted_items = DeletedItem.DeletedItem.select();

def update_cost_and_profit(_item):
    _item.buyTotalCost = _item.buySingleCost * _item.number;
    _item.sellTotalPrice = _item.sellSignlePrice * _item.number;
    _item.basicProfit = _item.sellTotalPrice - _item.buyTotalCost;
    _item.totalProfit = _item.basicProfit + _item.otherProfit - _item.otherCost;

def add_new_item(uID=0, name="", number=0, buySingleCost=0, buyTotalCost=0, \
    receivedNum=0, sellSignlePrice=0, sellTotalPrice = 0, receivedMoney=0, \
    otherCost=0, basicProfit=0, otherProfit=0, totalProfit=0, buyer="virus",\
     buyPlace="newegg", payCards="", ifDrop=False):
    new_item = Item(uID=uID, date=Lib.get_current_date(), name=name, number=number, buySingleCost=buySingleCost,\
        buyTotalCost = buyTotalCost, \
        sellSignlePrice=sellSignlePrice, sellTotalPrice=sellTotalPrice,\
        receivedMoney=receivedMoney, receivedNum=receivedNum, otherCost=otherCost,\
        basicProfit=basicProfit, otherProfit=otherProfit,\
        totalProfit=totalProfit, buyer=buyer, buyPlace=buyPlace, payCards=payCards,\
        ifDrop=ifDrop);

    if new_item.uID == 0:
    	new_item.uID = Lib.get_unique_ID();
    update_cost_and_profit(new_item);
    new_item.save();
    update_all_items();

def get_items_time_range(_start=datetime.date(1,1,1), _end=Lib.get_current_date()):
# def get_items_time_range(_start=Lib.get_current_date(), _end=Lib.get_current_date()):
    entries = Item.select().order_by(Item.date);
    ans = entries.where(Item.date >= _start);
    ans = ans.where(Item.date <= _end);
    return ans;


def get_item_by_ID(_ID):
    for x in Item.select():
        if x.uID == _ID:
            return x;

def delete_item_by_ID(_id):
    entries = Item.select().where(Item.uID == _id);
    for entry in entries:
        add_deleted_item(entry.uID);
        entry.delete_instance();
    update_all_items();

def delete_all_saved_items():
    for x in Item.select():
        x.delete_instance();

def add_deleted_item(_id):
    deleted_items = Item.select().where(Item.uID == _id);
    for newitem in deleted_items:
        new_deleted_item = DeletedItem.DeletedItem(uID=newitem.uID, date=newitem.date, name=newitem.name,\
            number=newitem.number, buySingleCost=newitem.buySingleCost, buyTotalCost=newitem.buyTotalCost,\
            sellSignlePrice=newitem.sellSignlePrice, sellTotalPrice=newitem.sellTotalPrice,\
            receivedMoney=newitem.receivedMoney, receivedNum=newitem.receivedNum, otherCost=newitem.otherCost,\
            basicProfit=newitem.basicProfit, otherProfit=newitem.otherProfit,\
            totalProfit=newitem.totalProfit, buyer=newitem.buyer, buyPlace=newitem.buyPlace, payCards=newitem.payCards,\
            ifDrop=newitem.ifDrop);
        update_cost_and_profit(new_deleted_item);
        new_deleted_item.save();

def copy_a_deleted_item(_deletedItem):
	'''return a Item the same as the _deletedItem'''
	add_new_item(uID=_deletedItem.uID);
