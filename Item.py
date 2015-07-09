import datetime
from peewee import *
import Lib
from MyDatabase import *
import DeletedItem

all_items = [];
item_list = [];

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
        order_by = ('-date',);

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
    _item.buyTotalCost = Lib.toDecimal(_item.buySingleCost * _item.number);
    _item.sellTotalPrice = Lib.toDecimal(_item.sellSignlePrice * _item.number);
    _item.basicProfit = Lib.toDecimal(_item.sellTotalPrice - _item.buyTotalCost);
    _item.totalProfit = Lib.toDecimal(_item.basicProfit + _item.otherProfit - _item.otherCost);

def add_new_item(uID=0, date=Lib.get_current_date(), name="", number=0, \
                buySingleCost=0, buyTotalCost=0, \
                receivedNum=0, sellSignlePrice=0, sellTotalPrice=0, receivedMoney=0, \
                otherCost=0, basicProfit=0, otherProfit=0, totalProfit=0, buyer="",\
                 buyPlace="", payCards="", ifDrop=False):
    new_item = Item(uID=uID, date=date, name=name, number=number, buySingleCost=Lib.toDecimal(buySingleCost),\
        buyTotalCost = Lib.toDecimal(buyTotalCost), \
        sellSignlePrice=Lib.toDecimal(sellSignlePrice), sellTotalPrice=sellTotalPrice,\
        receivedMoney=Lib.toDecimal(receivedMoney), receivedNum=receivedNum, otherCost=Lib.toDecimal(otherCost),\
        basicProfit=Lib.toDecimal(basicProfit), otherProfit=Lib.toDecimal(otherProfit),\
        totalProfit=Lib.toDecimal(totalProfit), buyer=buyer, buyPlace=buyPlace, payCards=payCards,\
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
	add_new_item(uID=_deletedItem.uID,\
                date=_deletedItem.date, number=_deletedItem.number, name=_deletedItem.name,\
                buySingleCost=_deletedItem.buySingleCost,\
                receivedNum=_deletedItem.receivedNum,\
                sellSignlePrice=_deletedItem.sellSignlePrice,\
                receivedMoney=_deletedItem.receivedMoney,\
                otherCost=_deletedItem.otherCost,\
                basicProfit=_deletedItem.basicProfit,\
                otherProfit=_deletedItem.otherProfit,\
                totalProfit=_deletedItem.totalProfit,\
                buyer=_deletedItem.buyer,\
                buyPlace=_deletedItem.buyPlace,\
                payCards=_deletedItem.payCards,\
                ifDrop=_deletedItem.ifDrop);
# -------------------------
#     items summary row
# --------------------------

def summary_item(_items):
    sumItem = {};
    sumItem['sumBuyTotalCost'] = 0;
    sumItem['sumSellTotalPrice'] = 0;
    sumItem['sumReceivedMoney'] = 0;
    sumItem['sumOtherCost'] = 0;
    sumItem['sumBasicProfit'] = 0;
    sumItem['sumOtherProfit'] = 0;
    sumItem['sumTotalProfit'] = 0;
    if (_items):
        for x in _items:
            sumItem['sumBuyTotalCost'] += x.buyTotalCost;
            sumItem['sumSellTotalPrice'] += x.sellTotalPrice;
            sumItem['sumOtherCost'] += x.otherCost;
            sumItem['sumBasicProfit'] += x.basicProfit;
            sumItem['sumOtherProfit'] += x.otherProfit;
            sumItem['sumTotalProfit'] += x.totalProfit;
            sumItem['sumReceivedMoney'] += x.receivedMoney;
    sumItem['sumBuyTotalCost'] = Lib.toDecimal(sumItem['sumBuyTotalCost']);
    sumItem['sumSellTotalPrice'] = Lib.toDecimal(sumItem['sumSellTotalPrice'] );
    sumItem['sumReceivedMoney'] = Lib.toDecimal(sumItem['sumReceivedMoney']);
    sumItem['sumOtherCost'] = Lib.toDecimal(sumItem['sumOtherCost']);
    sumItem['sumBasicProfit'] = Lib.toDecimal(sumItem['sumBasicProfit']);
    sumItem['sumOtherProfit'] = Lib.toDecimal(sumItem['sumOtherProfit']);
    sumItem['sumTotalProfit'] = Lib.toDecimal(sumItem['sumTotalProfit']);
    return sumItem;

def get_items_by_keyword(_keyword):
    del item_list[:];
    for x in all_items:
        itemstring = "";
        itemstring += x.name.strip().lower();
        itemstring += x.buyer.strip().lower();
        itemstring += x.buyPlace.strip().lower();
        itemstring += x.payCards.strip().lower();
        if _keyword in itemstring:
            item_list.append(x);
    return item_list;
    

