
import datetime
from peewee import *
from flask import (Flask, render_template, redirect, 
    url_for, request,  make_response, flash)
import json
import Lib

db = SqliteDatabase('all_purchased_items.db');

class Item(Model):
    ID = IntegerField();
    date = DateField();
    name = TextField();
    number = 0;
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
    db.connect();
    db.create_tables([Item], safe=True);

def update_all_items():
    global all_items;
    all_items = Item.select();

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
    for x in all_items:
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

#####################Network###########################
#####################Network###########################
#####################Network###########################

app = Flask(__name__);
init_database();
all_items = Item.select();
deleted_items = [];

@app.route('/')
def index(saves=""):
    return render_template("index.html", saves=saves, date=Lib.get_current_date());

@app.route('/selected_items', methods=['POST'])
def selected_items():
    data = {};
    data.update(dict(request.form.items()));
    print data;
    # date1 = datetime.date(Lib.toInt(data['syear']), Lib.toInt(data['smonth'])\
    #     , Lib.toInt(data['sday']));
    # date2 = datetime.date(Lib.toInt(data['eyear']), Lib.toInt(data['emonth'])\
    #     , Lib.toInt(data['eday']));
    # ans = get_items_time_range(date1, date2);
    response = make_response(redirect(url_for('index')));
    # response.set_cookie('character', json.dumps(data));
    return response;

@app.route('/show_all_items')
def show_all_items():
    return render_template("show_all_items.html", all_items=all_items);

@app.route('/add_item')
def add_item():
    return render_template("add_item.html", all_items=all_items);

def get_saved_data():
    try:
        data = json.loads(request.cookies.get('character'));
    except TypeError:
        data = {};
    return data;

@app.route('/save_new_item', methods=['POST'])
def save_new_item():
    data = {};
    data.update(dict(request.form.items()));
    add_new_item(_name=data['name'], _number=Lib.toInt(data['num']), \
        _buySingleCost=Lib.toFloat(data['buySingleCost']),\
        _sellSignlePrice=Lib.toFloat(data['sellSignlePrice']),\
         _otherCost=Lib.toFloat(data['otherCost']),\
         _otherProfit=Lib.toFloat(data['otherProfit']),\
          _buyer=data['buyer'], _buyPlace=data['buyPlace'],\
        _payCards=data['payCards']);
    response = make_response(redirect(url_for('show_all_items')));
    # response.set_cookie('character', json.dumps(data));
    return response;

@app.route('/delete_item', methods=['POST'])
def delete_item():
    data = {};
    data.update(dict(request.form.items()));
    delete_item_by_ID(Lib.toInt(data['delete']));
    response = make_response(redirect(url_for('show_all_items')));
    # response.set_cookie('character', json.dumps(data));
    return response;

@app.route('/jump_revise_item', methods=['POST'])
def jump_revise_item():
    data = {};
    data.update(dict(request.form.items()));
    response = make_response(redirect(url_for('revise_item', ID=data['revise'])));
    # response.set_cookie('character', json.dumps(data));
    return response;

@app.route('/revise_item/<int:ID>')
@app.route('/revise_item')
def revise_item(ID=-1):
    item = get_item_by_ID(ID);
    return render_template("revise_item.html", item=item);

@app.route('/save_revise_item', methods=['POST'])
def save_revise_item():
    data = {};
    data.update(dict(request.form.items()));
    ID = Lib.toInt(data['ID']);
    for x in all_items:
        if x.ID == ID:
            x.name = data['name'];
            x.number = Lib.toInt(data['num']);
            x.buySingleCost = Lib.toFloat(data['buySingleCost']);
            x.receivedNum = Lib.toInt(data['receivedNum']);
            x.sellSignlePrice = Lib.toFloat(data['sellSignlePrice']);
            x.receivedMoney = Lib.toFloat(data['receivedMoney']);
            x.otherCost = Lib.toFloat(data['otherCost']);
            x.otherProfit = Lib.toFloat(data['otherProfit']);
            x.buyer = data['buyer'];
            x.ifDrop = data['ifDrop'];
            x.buyPlace = data['buyPlace'];
            x.payCards = data['payCards'];
            update_cost_and_profit(x);

    response = make_response(redirect(url_for('show_all_items')));
    # response.set_cookie('character', json.dumps(data));
    return response;

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8000);
        
