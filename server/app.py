#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from sqlalchemy import desc

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():

    bakeries = []

    for bakery in Bakery.query.all():
        bakeries_dict = {
            'id': bakery.id,
            'name': bakery.name,
            'created_at': bakery.created_at
        }
        bakeries.append(bakeries_dict)
    
    response = make_response(
        jsonify(bakeries),
        200)

    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    
    bakery = Bakery.query.filter(Bakery.id==id).first()

    bakery_dict = bakery.to_dict()

    response = make_response(
        jsonify(bakery_dict),
        200
    )
    response.headers["Content-Type"] = "application/json"

    return response


@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    
    goods = []

    for baked_good in BakedGood.query.order_by(desc(BakedGood.price)):
        baked_goods_dict = {
            'id': baked_good.id,
            'name': baked_good.name,
            'price': baked_good.price,
            'created_at': baked_good.created_at
        }
        goods.append(baked_goods_dict)
    
    response = make_response(
        jsonify(goods),
        200
    )
    
    response.headers["Content-Type"] = "application/json"

    return response


@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():

    most_expensive = BakedGood.query.order_by(desc(BakedGood.price)).first()
    
    baked_goods_dict = {
        'id': most_expensive.id,
        'name': most_expensive.name,
        'price': most_expensive.price,
        'created_at': most_expensive.created_at
    }
    
    response = make_response(
        jsonify(baked_goods_dict),
        200
    )
    
    response.headers["Content-Type"] = "application/json"

    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
