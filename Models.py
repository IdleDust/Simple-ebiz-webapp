import datetime
from peewee import *

import Lib

db = SqliteDatabase('all_purchased_items.db');
all_items = None;
deleted_items = [];

class Item(Model):
    ID = IntegerField();
    date = DateField();
    name = TextField();
    number = 0; #IntegerField(default=0);
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
    # db = SqliteDatabase('all_purchased_items.db');
    deleted_items = [];
    db.connect();
    db.create_tables([Item], safe=True);
    all_items = Item.select();

def update_all_items():
    global all_items;
    all_items = Item.select();

def update_ID(_item):
    _item.ID = 0;
    entries = Item.select().order_by(Item.ID.desc());
    for entry in entries:
        _item.ID = entry.ID + 1;
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
        if x.ID == _ID:
            return x;

def input_a_new_item():
    name = raw_input('Input the name: ').strip();
    add_new_item(_name = name, _date=Lib.get_current_date());

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

def add_new_item(_ID=0, _date=Lib.get_current_date(), _name="", _number=0, _buySingleCost=0, _buyTotalCost=0, _receivedNum=0, _sellSignlePrice=0, _sellTotalPrice = 0, _receivedMoney=0, _otherCost=0, _basicProfit=0, _otherProfit=0, _totalProfit=0, _buyer="virus", _buyPlace="newegg",\
 _payCards="",_ifDrop=False):
    new_item = Item(ID=_ID, date=_date, name=_name, number =_number, buySingleCost=_buySingleCost,\
        buyTotalCost = _buyTotalCost, receivedNum=_receivedNum, \
        sellSignlePrice=_sellSignlePrice, sellTotalPrice=_sellTotalPrice,\
        receivedMoney=_receivedMoney, otherCost=_otherCost,\
        basicProfit=_basicProfit, otherProfit=_otherProfit,\
        totalProfit=_totalProfit, buyer=_buyer, buyPlace=_buyPlace, payCards=_payCards,\
        ifDrop=_ifDrop);

    update_cost_and_profit(new_item);
    update_ID(new_item);
    new_item.save();
    update_all_items();



