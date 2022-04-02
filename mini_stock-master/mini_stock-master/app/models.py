#  db是在app/__init__.py生成的关联后的SQLAlchemy实例
import datetime
import decimal
import json
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import relationship

from app import db


# 用户表
class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(255))
    email = db.Column(db.String(50))
    mobile_phone = db.Column(db.String(11))
    user_type = db.Column(db.String(1), default='U')
    status = db.Column(db.SmallInteger, default='0')

    # repr()方法显示一个可读字符串
    def __repr__(self):
        return 'User:%s' % self.user_name


#  帐户表
class Account(db.Model):
    __tablename__ = 'accounts'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    account_name = db.Column(db.String(50))
    account = db.Column(db.String(20), unique=True)
    bank_name = db.Column(db.String(20))
    bank_account = db.Column(db.String(50))
    balance = db.Column(db.Numeric(15, 3), default=0)
    accu_earning = db.Column(db.Numeric(18, 3), default=0)
    total_earning = db.Column(db.Numeric(18, 3), default=0)
    stock_cost = db.Column(db.Numeric(18, 3), default=0)
    stock_value = db.Column(db.Numeric(18, 3), default=0)
    open_date = db.Column(db.Date)

    # repr()方法显示一个可读字符串
    def __repr__(self):
        return 'Account:%s' % self.account_name


#  股票信息表
class Stock(db.Model):
    __tablename__ = 'stocks'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    stock_code = db.Column(db.String(10), unique=True)
    stock_name = db.Column(db.String(30))
    stock_type = db.Column(db.String(30))
    company_name = db.Column(db.String(50))
    company_brief = db.Column(db.Text)
    address = db.Column(db.String(200))
    reg_capital = db.Column(db.Float())
    issue_price = db.Column(db.Numeric(10, 3))
    total_number = db.Column(db.Integer)
    current_price = db.Column(db.Numeric(10, 3))
    total_value = db.Column(db.Float())
    pe_ratio = db.Column(db.Numeric(10, 3))

    # repr()方法显示一个可读字符串
    def __repr__(self):
        return 'Stock:%s' % self.stock_name


#  个人持股余额信息
class AccountStock(db.Model):
    __tablename__ = 'account_stocks'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(20), db.ForeignKey('accounts.account'))
    stock_code = db.Column(db.String(10), db.ForeignKey('stocks.stock_code'))
    number = db.Column(db.Integer)
    cost = db.Column(db.Numeric(10, 3))

#  股票交易记录表
class Trade(db.Model):
    __tablename__ = 'trades'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(20), db.ForeignKey('accounts.account'))
    stock_code = db.Column(db.String(10), db.ForeignKey('stocks.stock_code'))
    trade_type = db.Column(db.String(1))
    number = db.Column(db.Integer)
    trade_price = db.Column(db.Numeric(10, 3))
    trade_time = db.Column(db.DateTime)


class AlchemyEncoder(json.JSONEncoder):
    """
    SqlAlchemy对象转换为json格式
    """

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                # print(type(data), data)
                try:
                    json.dumps(data)  # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:  # 添加了对datetime的处理
                    if isinstance(data, datetime.datetime):
                        fields[field] = data.strftime("%Y-%m-%d %H:%M:%S")
                    elif isinstance(data, datetime.date):
                        fields[field] = data.strftime('%Y-%m-%d')
                    elif isinstance(data, datetime.time):
                        fields[field] = data.isoformat()
                    elif isinstance(data, decimal.Decimal):
                        # print("wujize test encoder")
                        # print(float(data))
                        fields[field] = float(data)
                    # TODO 下边的有问题，还需要修正,原来目的是循环自定义类型
                    # else:
                    #     fields[field] = AlchemyEncoder.default(self, data)
            return fields
        return json.JSONEncoder.default(self, obj)
