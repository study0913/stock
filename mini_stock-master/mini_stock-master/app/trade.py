from flask import Blueprint, request, flash, session
from app import db
import datetime
import json
from app.models import User, Account, AccountStock, Trade, AlchemyEncoder
from app.myget_stock import get_rt_hq

trade = Blueprint("trade", __name__)


#  获取用户某账户交易详情信息,返回帐户名称，帐户余额，股票最新价格，股票持仓数量，收益。
@trade.route('/get_by_account', methods=['get', 'post'])
def get_by_account():
    param = request.get_data()
    if param:
        param = json.loads(param)
        print(param)
        stock_code = param['stock_code']
        # 根据session查找用户ID
        user_name = session.get('username')
        user_id = User.query.filter(User.user_name == user_name).first().id
        # 根据用户ID查找用户的account号
        account1 = Account.query.filter(Account.user_id == user_id).first()
        if account1:
            stock_number = 0
            stock_cost = 0
            # 根据account帐户与股票代码，查找帐户该股票的持仓数量
            if stock_code:
                trade_account = AccountStock.query.filter_by(
                    account=account1.account, stock_code=stock_code).first()
                if trade_account:
                    stock_number = trade_account.number
                    stock_cost = trade_account.cost
            # 构建返回的json字典,注意对日期，decimal要进行转换处理
            result = {'account': account1.account, 'account_name': account1.account_name,
                      'balance': float(account1.balance), 'stock_number': stock_number, 'stock_cost': float(stock_cost)}
            print(result)
            return result
        else:
            print("用户没有帐号户，不能进行交易")
            return "用户没有帐号户，不能进行交易", 400
    print("前后端参数传递错误，请联系系统员解决")
    return "前后端参数传递错误，请联系系统员解决", 400


#  股票买入交易事务。
@trade.route('/buy_stock', methods=['get', 'post'])
def buy_stock():
    param = request.get_data()
    if param:
        param = json.loads(param)
        print(param)
        stock_code = param['stock_code']
        account = param['account']
        trade_number = int(param['trade_number'])
        price = float(param['price'])
        now_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 获取最新价格，判断提交的价格是否低于最新行情，低于对应反馈信息
        hq = get_rt_hq(stock_code)
        rt_price = float(hq[3])
        if price < rt_price:
            return "输入的交易价格低于最新行情价格，交易不成功!", 400
            print("输入的交易价格低于最新行情价格，交易不成功!")
        # 构建交易事务
        trade1 = Trade()
        trade1.account = account
        trade1.stock_code = stock_code
        trade1.number = trade_number
        trade1.trade_type = 'B'
        trade1.trade_price = price
        trade1.trade_time = now_date
        # 判断帐户可用资金余额是否可以完成此笔交易
        account_record = Account.query.filter(Account.account == account).first()
        if account_record.balance < trade_number * price:
            return "帐户资金余额不足，不能完成此次交易", 400
        account_record.balance = float(account_record.balance) - trade_number * price
        # 查询帐户持股是否有此股票，有增加数据更新，没有添加新记录
        account_stock = AccountStock.query.filter_by(
            account=account, stock_code=stock_code).first()
        if account_stock:
            #  已持有该股票在记录，更新
            have_number = int(account_stock.number)
            have_cost = float(account_stock.cost)
            account_stock.number = have_number + trade_number
            account_stock.cost = (have_number * have_cost + trade_number * price) / (have_number + trade_number)
            try:
                db.session.add(trade1)
                db.session.commit()
                return '股票买入交易成功！'
            except Exception as e:
                db.session.rollback()
                return '股票买入交易失败1！！！', 400
        else:
            #  尚未持有过该股票，添加
            account_stock1 = AccountStock()
            account_stock1.account = account
            account_stock1.stock_code = stock_code
            account_stock1.number = trade_number
            account_stock1.cost = price
            print(json.dumps(trade1, cls=AlchemyEncoder))
            print(json.dumps(account_stock1, cls=AlchemyEncoder))
            print(json.dumps(account_record, cls=AlchemyEncoder))
            try:
                db.session.add(trade1)
                db.session.add(account_stock1)
                db.session.commit()
                return '股票买入交易成功！'
            except Exception as e:
                db.session.rollback()
                return '股票买入交易失败2！！！', 400

    print("前后端参数传递错误，请联系系统员解决")
    return "前后端参数传递错误，请联系系统员解决", 400


#  股票卖出交易事务。
@trade.route('/sell_stock', methods=['get', 'post'])
def sell_stock():
    param = request.get_data()
    if param:
        param = json.loads(param)
        print(param)
        stock_code = param['stock_code']
        account = param['account']
        trade_number = int(param['trade_number'])
        price = float(param['price'])
        now_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 获取最新价格，判断提交的价格是否低于最新行情，低于对应反馈信息
        hq = get_rt_hq(stock_code)
        rt_price = float(hq[3])
        if price > rt_price:
            return "输入的交易价格高于最新行情价格，交易不成功!", 400
            print("输入的交易价格高于最新行情价格，交易不成功!")
        # 构建交易事务
        trade2 = Trade()
        trade2.account = account
        trade2.stock_code = stock_code
        trade2.number = trade_number
        trade2.trade_type = 'S'
        trade2.trade_price = price
        trade2.trade_time = now_date
        account_stock = AccountStock.query.filter_by(account=account, stock_code=stock_code).first()
        if account_stock:
            have_number = int(account_stock.number)
            # 判断帐户持仓数据是否大于交易请求数据
            if have_number < trade_number:
                return "帐户持仓数量不足，不能完成此次交易", 400
            #  已持有该股票在记录，更新剩余数量
            have_cost = float(account_stock.cost)
            account_stock.number = have_number - trade_number

            # 更新账户余额，累计收益
            account_record2 = Account.query.filter(Account.account == account).first()
            have_balance = float(account_record2.balance)
            have_earning = float(account_record2.accu_earning)

            account_record2.balance = have_balance + (trade_number * price)
            account_record2.accu_earning = have_earning + trade_number * (price - have_cost)
            # 如果持仓数大于交易数，减少持仓数量，累计收益，加回余额后，如等于删除记录
            if have_number > trade_number:
                # 卖出不需要更新持仓成本
                # account_stock.cost = (have_number * have_cost - trade_number * price) / (have_number - trade_number)
                try:
                    db.session.add(trade2)
                    db.session.commit()
                    return '股票买入交易成功！'
                except Exception as e:
                    db.session.rollback()
                    return '股票买入交易失败1！！！', 400
            else:
                account_stock.cost
                try:
                    db.session.add(trade2)
                    db.session.delete(account_stock)
                    db.session.commit()
                    return '股票买入交易成功！'
                except Exception as e:
                    db.session.rollback()
                    return '股票买入交易失败2！！！', 400
        else:
            #  尚未持有过该股票，添加
            return "没有查到持仓股票，交易失败", 400

    print("前后端参数传递错误，请联系系统员解决")
    return "前后端参数传递错误，请联系系统员解决", 400
