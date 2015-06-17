import datetime
from peewee import *
import Lib

db = SqliteDatabase('all_purchased_items.db');
all_items = None;
deleted_items = [];

class Item(Model):
    uID = IntegerField();
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


def init_database():
    global all_items;
    global db;
    global deleted_items;
    db = SqliteDatabase('all_purchased_items.db');
    deleted_items = [];
    db.connect();
    db.create_tables([Item], safe=True);
    all_items = Item.select();

def update_all_items():
    global all_items;
    all_items = Item.select();

def update_ID(_item):
    _item.uID = 0;
    a = Item.select().order_by(Item.uID.desc());
    for x in a:
        _item.uID = x.uID + 1;
        break;

def update_cost_and_profit(_item):
    _item.buyTotalCost = _item.buySingleCost * _item.number;
    _item.sellTotalPrice = _item.sellSignlePrice * _item.number;
    _item.basicProfit = _item.sellTotalPrice - _item.buyTotalCost;
    _item.totalProfit = _item.basicProfit + _item.otherProfit - _item.otherCost;

def get_items_time_range(_start=datetime.date(1,1,1), _end=Lib.get_current_date()):
    entries = Item.select().order_by(Item.date);
    ans = entries.where(Item.date >= _start);
    ans = ans.where(Item.date <= _end);
    return ans;

def get_item_by_ID(_ID):
    for x in Item.select():
        if x.uID == _ID:
            return x;

def delete_all_items():
    for x in Item.select():
        x.delete_instance();

def delete_item_by_ID(_id):
    global deleted_items;
    entries = Item.select().where(Item.ID == _id);
    for entry in entries:
        deleted_items.append(entry);
        entry.delete_instance();
    update_all_items();

def add_new_item(ID=0, date=Lib.get_current_date(), name="", number=0, buySingleCost=0, buyTotalCost=0, \
    receivedNum=0, sellSignlePrice=0, sellTotalPrice = 0, receivedMoney=0, \
    otherCost=0, basicProfit=0, otherProfit=0, totalProfit=0, buyer="virus",\
     buyPlace="newegg", payCards="", ifDrop=False):
    new_item = Item(uID=ID, date=date, name=name, number=number, buySingleCost=buySingleCost,\
        buyTotalCost = buyTotalCost, \
        sellSignlePrice=sellSignlePrice, sellTotalPrice=sellTotalPrice,\
        receivedMoney=receivedMoney, receivedNum=receivedNum, otherCost=otherCost,\
        basicProfit=basicProfit, otherProfit=otherProfit,\
        totalProfit=totalProfit, buyer=buyer, buyPlace=buyPlace, payCards=payCards,\
        ifDrop=ifDrop);

    update_cost_and_profit(new_item);
    update_ID(new_item);
    new_item.save();
    update_all_items();

def input_new_item():
    n = int(raw_input('Input a number: '));
    p1 = int(raw_input('Input buy price: '));
    p2 = int(raw_input('Input sell price: '));
    add_new_item( buySingleCost=p1, sellSignlePrice=p2);

def print_all_items():
    all_items = Item.select();
    for x in all_items:
        print x.uID, x.buySingleCost, x.sellSignlePrice;

if __name__ == '__main__':
    init_database();
    input_new_item();
    print_all_items();

