from flask import Blueprint, request, flash, session
from app import db
import json
from app.models import Account, AccountStock, User, AlchemyEncoder
import datetime

account = Blueprint("account", __name__)


#  获取用户的帐户信息
@account.route('/get_by_user', methods=['get', 'post'])
def get_by_user():
    param = request.get_data()
    if param:
        param = json.loads(param)
        print(param)
        user_id = param['user_id']
        account1 = Account.query.filter(Account.user_id == user_id).first()
        return json.dumps(account1, cls=AlchemyEncoder)
    print("前后端参数传递错误，请联系系统员解决")
    return "前后端参数传递错误，请联系系统员解决", 400


#  添加或更新用户帐户信息,开户
@account.route('/open_account', methods=['post'])
def open_account():
    param = request.get_data()
    if param:
        param = json.loads(param)
        print(param)
        if param['account_id']:
            Account.query.filter(Account.id == param['account_id']).update({"account_name": param['account_name'],
                                                                            "account": param['account'],
                                                                            "bank_name": param['bank_name'],
                                                                            "bank_account": param['bank_account']
                                                                            })
            db.session.commit()
            return '帐户信息修改成功！'
        else:
            account1 = Account()
            account1.user_id = param['user_id']
            account1.account_name = param['account_name']
            account1.account = param['account']
            account1.bank_name = param['bank_name']
            account1.bank_account = param['bank_account']
            # 帐户初始化时，充入100000万
            account1.balance = 100000
            now_date = datetime.datetime.now().strftime("%Y-%m-%d")
            account1.open_date = now_date
            try:
                db.session.add(account1)
                db.session.commit()
                return '用户添加成功！'
            except Exception as e:
                db.session.rollback()
                return '用户数据有问题，添加失败！！！', 400
    else:
        print("前后端参数传递错误，请联系系统员解决")
        return "前后端参数传递错误，请联系系统员解决", 400


#  获取用户帐号及某支股票的持仓信息
@account.route('/get_account_stock', methods=['get', 'post'])
def get_account_stock():
    param = request.get_data()
    if param:
        param = json.loads(param)
        print(param)
        account1 = param['account']
        stock_code1 = param['stock_code']
        account1 = AccountStock.query.filter(
            AccountStock.account == account1 and AccountStock.stock_code == stock_code1).first()
        return json.dumps(account1, cls=AlchemyEncoder)
    else:
        print("前后端参数传递错误，请联系系统员解决")
        return "前后端参数传递错误，请联系系统员解决", 400


#  获取用户帐号所有股票的持仓信息
@account.route('/get_stock_list', methods=['get', 'post'])
def get_stock_list():
    param = request.get_data()
    if param:
        param = json.loads(param)
        print(param)
        account1 = param['account']
        sql = "SELECT account_stocks.id AS id, " \
              "account_stocks.account AS account, " \
              "account_stocks.stock_code AS stock_code, " \
              "account_stocks.number AS number, " \
              "account_stocks.cost AS cost," \
              "stocks.stock_name as stock_name," \
              "stocks.current_price as current_price" \
              " FROM account_stocks,stocks" \
              " WHERE account_stocks.stock_code = stocks.stock_code " \
              "and account_stocks.account = :account_1"
        #  返回的是rawProxy对象，还需要转为前端可以接受的Dict
        stock_list = db.session.execute(sql, {'account_1': account1})
        list1 = list(stock_list)
        ret_list = []
        for stock in list1:
            item = {'id': stock[0],
                    'account': stock[1],
                    'stock_code': stock[2],
                    'number': float(stock[3]),
                    'cost': float(stock[4]),
                    'stock_name': stock[5],
                    'current_price': float(stock[6])
                    }
            ret_list.append(item)
        print(ret_list)
        # stock_list = AccountStock.query.filter(
        #     AccountStock.account == account1).all()
        return json.dumps(ret_list, cls=AlchemyEncoder)
    else:
        print("前后端参数传递错误，请联系系统员解决")
        return "前后端参数传递错误，请联系系统员解决", 400


#  先计算所有帐号的持仓收益，然后返回所有帐号收益排名
@account.route('/get_all_earning')
def get_all_earning():
    print("后台定时任务，更新持仓收益")
    account_list = Account.query.all()
    for account1 in account_list:
        account_number = account1.account
        sql = "select sum(stock_earning) as stock_earnings," \
              "sum(cost*number) as stock_cost," \
              "sum(current_price*number) as stock_value" \
              " from account_stat where account = :account_1"
        stock_earnings = db.session.execute(sql, {'account_1': account_number}).fetchone()
        list2 = list(stock_earnings)
        if list2[0]:
            account1.total_earning = float(list2[0]) + float(account1.accu_earning)
            account1.stock_cost = float(list2[1])
            account1.stock_value = float(list2[2])
        else:
            account1.total_earning = account1.accu_earning
            account1.stock_cost = 0
            account1.stock_value = 0
    db.session.commit()


#  根据收益总收益名称，返回帐户清单
@account.route('/get_by_earning', methods=['get', 'post'])
def get_by_earning():
    account_list = Account.query.order_by(Account.total_earning.desc()).all()
    return json.dumps(account_list, cls=AlchemyEncoder)


#  根据帐户号获得用户投资组合数据，如account号为空，则先取当前用户
@account.route('/investment_stat')
def investment_stat():
    # 根据session获取用户与account
    user_name = session.get('username')
    user1 = User.query.filter(User.user_name == user_name).first()
    account1 = Account.query.filter(Account.user_id == user1.id).first()
    # 先将用户帐户余额添加到返回数组
    ret_list = [{'name': '帐户余额', 'value': float(account1.balance)}]
    # 查询帐户持仓数据
    sql = "SELECT account_stocks.id AS id, " \
          "account_stocks.account AS account, " \
          "account_stocks.stock_code AS stock_code, " \
          "account_stocks.number AS number, " \
          "account_stocks.cost AS cost," \
          "stocks.stock_name as stock_name," \
          "stocks.current_price as current_price" \
          " FROM account_stocks,stocks" \
          " WHERE account_stocks.stock_code = stocks.stock_code " \
          "and account_stocks.account = :account_1"
    #  返回的是rawProxy对象，还需要转为前端可以接受的Dict
    stock_list = db.session.execute(sql, {'account_1': account1.account})
    list1 = list(stock_list)

    for stock in list1:
        item = {'name': stock[5], 'value': int(float(stock[6]) * float(stock[3]))
                }
        ret_list.append(item)
    print(ret_list)
    # stock_list = AccountStock.query.filter(
    #     AccountStock.account == account1).all()
    return json.dumps(ret_list, cls=AlchemyEncoder)
