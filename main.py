from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship

from utils import read_json, users_instance_to_dict, orders_instance_to_dict, offers_instance_to_dict

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.url_map.strict_slashes = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    age = Column(Integer)
    email = Column(String)
    role = Column(String)
    phone = Column(String)


class Offer(db.Model):
    __tablename__ = 'offer'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("order.id"))
    executor_id = Column(Integer, ForeignKey("user.id"))

    user = relationship("User")
    order = relationship("Order")


class Order(db.Model):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    start_date = Column(String)
    end_date = Column(String)
    address = Column(String)
    price = Column(Integer)
    customer_id = Column(Integer)
    executor_id = Column(Integer, ForeignKey("user.id"))

    user = relationship("User")


def add_data_to_users():
    file_name = './users.json'
    data_json = read_json(file_name)
    for item in data_json:
        user = User(
            **item
            # id=item.get('id'),
            # first_name=item.get('first_name'),
            # last_name=item.get('last_name'),
            # age=item.get('age'),
            # email=item.get('email'),
            # role=item.get('role'),
            # phone=item.get('phone')
        )
        db.session.add(user)
    db.session.commit()
    return data_json


def add_data_to_orders():
    file_name = './orders.json'
    data_json = read_json(file_name)
    for item in data_json:
        order = Order(
            **item
            # id=item.get('id'),
            # name=item.get('name'),
            # description=item.get('description'),
            # start_date=item.get('start_date'),
            # end_date=item.get('end_date'),
            # address=item.get('address'),
            # price=item.get('price'),
            # customer_id=item.get('customer_id'),
            # executor_id=item.get('executor_id')
        )
        db.session.add(order)
    db.session.commit()
    return data_json


def add_data_to_offers():
    file_name = './offers.json'
    data_json = read_json(file_name)
    for item in data_json:
        offer = Offer(
            **item
            # id=item.get('id'),
            # order_id=item.get('order_id'),
            # executor_id=item.get('executor_id')
        )
        db.session.add(offer)
    db.session.commit()
    return data_json


with app.app_context():
    db.init_app(app)
    db.drop_all()
    db.create_all()
    add_data_to_users()
    add_data_to_orders()
    add_data_to_offers()


@app.route('/users')
def page_users():
    users = User.query.all()
    result = []
    for item in users:
        result.append(users_instance_to_dict(item))
    return jsonify(result)


@app.route('/users/<id>')
def page_user(id):
    users = User.query.filter(User.id == id).all()
    result = []
    for item in users:
        result.append(users_instance_to_dict(item))
    return jsonify(result)


@app.route('/orders')
def page_orders():
    orders = Order.query.all()
    result = []
    for item in orders:
        result.append(orders_instance_to_dict(item))
    return jsonify(result)


@app.route('/orders/<id>')
def page_order(id):
    orders = Order.query.filter(Order.id == id).all()
    result = []
    for item in orders:
        result.append(orders_instance_to_dict(item))
    return jsonify(result)


@app.route('/offers')
def page_offers():
    offers = Offer.query.all()
    result = []
    for item in offers:
        result.append(offers_instance_to_dict(item))
    return jsonify(result)


@app.route('/offers/<id>')
def page_offer(id):
    offers = Offer.query.filter(Offer.id == id).all()
    result = []
    for item in offers:
        result.append(offers_instance_to_dict(item))
    return jsonify(result)


@app.post('/users')
def page_users_post():
    data = request.json
    user = User(
        id=data.get('id'),
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        age=data.get('age'),
        email=data.get('email'),
        role=data.get('role'),
        phone=data.get('phone'),
    )
    db.session.add(user)
    db.session.commit()
    return jsonify(data)


@app.put('/users/<bid>')
def page_user_put(bid):
    data = request.json
    user_to_update = db.session.query(User).get(bid)
    user_to_update.id = data.get('id')
    user_to_update.first_name = data.get('first_name')
    user_to_update.last_name = data.get('last_name')
    user_to_update.age = data.get('age')
    user_to_update.email = data.get('email')
    user_to_update.phone = data.get('phone')
    # db.session.add(user_to_update)
    db.session.commit()
    return 'Ok'


@app.delete('/users/<id>')
def page_user_delete(id):
    user_to_delete = User.query.get(id)
    db.session.delete(user_to_delete)
    db.session.commit()
    return jsonify(users_instance_to_dict(user_to_delete))


if __name__ == '__main__':
    app.run(port=8081)
