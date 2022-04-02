from flask import Blueprint, request, session,  render_template, flash
from hashlib import md5
from app.models import User

auth = Blueprint("auth", __name__)


#  用户登录
@auth.route('/login', methods=['get', 'post'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    password2 = md5(password.encode('utf8')).hexdigest()
    session.permanent = True
    result = User.query.filter(User.user_name == username, User.password == password2).first()

    if result:
        if result.status == 0:
            session['username'] = username
            return render_template("index.html")
        else:
            flash("帐号已冻结，不允许登录！")
            return render_template("login.html")
    else:
        flash("用户名或密码不正确！")
        return render_template("login.html")


@auth.route('/logout')
def logout():
    print(session)
    if 'username' in session:
        del session['username']
    return render_template("login.html")
