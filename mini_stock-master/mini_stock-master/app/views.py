from flask import request,Blueprint, render_template, session, flash, redirect
from app import app
from app.user import get_type
from PIL import Image
views = Blueprint("views", __name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')


@views.route('/user')
def user():
    #  只有admin或管理员用户可以管理用户，T
    user_name = session['username']
    user_type = get_type(user_name)
    if (user_name == 'admin') | (user_type == 'M'):
        return render_template("user.html")
    else:
        flash("没有权限使用用户管理模块！")
        return redirect('/')


@views.route('/stock')
def stock():
    return render_template("stock.html")

@views.route('/history',methods=['GET','POST'])
def history():
    if request.method == 'GET':
        return render_template('history.html')
    else:
        stock_code=str(request.get_data(),'utf-8')
        realtime = "http://image.sinajs.cn/newchart/min/n/sh"+stock_code+".gif"
        weekly = "http://image.sinajs.cn/newchart/daily/n/sh"+stock_code+".gif"
        monthly= "http://image.sinajs.cn/newchart/weekly/n/sh"+stock_code+".gif"
        yearly = "http://image.sinajs.cn/newchart/monthly/n/sh"+stock_code+".gif"
        from urllib.request import urlretrieve
        urlretrieve(realtime, './app/static/images/realtime.gif')
        urlretrieve(weekly, './app/static/images/weekly.gif')
        urlretrieve(monthly, './app/static/images/monthly.gif')
        urlretrieve(yearly, './app/static/images/yearly.gif')
        return render_template('history.html')


@views.route('/trade')
def trade():
    return render_template("trade.html")


@views.route('/stat')
def stat():
    return render_template("stat.html")