
import datetime
from peewee import *
from flask import (Flask, render_template, redirect, 
    url_for, request,  make_response, flash)
import json
import Lib
import Models


app = Flask(__name__);


@app.route('/')
def index(saves=""):
    return render_template("index.html", saves=saves, date=Lib.get_current_date());

@app.route('/selected_items', methods=['POST'])
def selected_items():
    data = {};
    data.update(dict(request.form.items()));
    print (data)
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
    print("shit");
    return render_template("show_all_items.html", all_items=Models.all_items);

@app.route('/add_item')
def add_item():
    return render_template("add_item.html", all_items=Models.all_items);

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
    Models.add_new_item(_name=data['name'], _number=data['num'], \
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
    Models.delete_item_by_ID(Lib.toInt(data['delete']));
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
    item = Models.get_item_by_ID(ID);
    return render_template("revise_item.html", item=item);

@app.route('/save_revise_item', methods=['POST'])
def save_revise_item():
    data = {};
    data.update(dict(request.form.items()));
    ID = Lib.toInt(data['ID']);
    for x in Models.all_items:
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
            Models.update_cost_and_profit(x);

    response = make_response(redirect(url_for('show_all_items')));
    # response.set_cookie('character', json.dumps(data));
    return response;

if __name__ == '__main__':
    Models.init_database();
    app.run(debug=True, host='127.0.0.1', port=8000);
        
