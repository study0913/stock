from app import app
from app import db
from flask import request, session, render_template
from flask_apscheduler import APScheduler  # 引入APScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from app.views import views
from app.auth import auth
from app.user import user
from app.stock import stock, update_hq
from app.account import account, get_all_earning
from app.trade import trade


#  访问内容前验证是否登录
@app.before_request
def before_request():
    if request.path == "login.html" or request.path == "/auth/login" or request.path.endswith(
            ".js") or request.path.endswith(".css") or request.path.endswith(".ico"):
        pass
    else:
        username = session.get('username')
        if not username:
            return render_template("login.html")


#  注册模块蓝图
app.register_blueprint(views, url_prefix="/views")
app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(user, url_prefix="/user")
app.register_blueprint(stock, url_prefix="/stock")
app.register_blueprint(account, url_prefix="/account")
app.register_blueprint(trade, url_prefix="/trade")

if __name__ == "__main__":
    # 启动前同步一下股票行情数据,更新一下帐户收益
    with app.app_context():
        db.create_all()
    update_hq()
    get_all_earning()
    # 执行定时任务
    scheduler = APScheduler()                  # 实例化 APScheduler
    # it is also possible to enable the API directly
    # scheduler.api_enabled = True
    scheduler = APScheduler(BackgroundScheduler(timezone="Asia/Shanghai"))
    scheduler.init_app(app)                    # 把任务列表放入 flask
    scheduler.start()

    app.run()
