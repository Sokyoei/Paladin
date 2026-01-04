from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from flask_learn.config import login_manager
from flask_learn.crud.user import UserCRUD
from flask_learn.schemas.login import LoginForm

bp = Blueprint('login', __name__)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    # 如果已经登陆，跳转到 dashboard
    if current_user.is_authenticated:
        return redirect(url_for('login.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = UserCRUD.get_user_by_email(email, orm=True)
        if user and user.verify_password(password):
            login_user(user, remember=form.remember_me.data)
            flash('登录成功！', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        flash('用户名或密码错误', 'danger')
    return render_template('login.html')


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('已登出', 'success')
    return redirect(url_for('login.login'))


@bp.route('/dashboard')
@login_required
def dashboard():
    """个人页面"""
    return render_template('dashboard.html', user=current_user)


@login_manager.unauthorized_handler
def unauthorized():
    """未登录重定向到登陆界面"""
    return redirect(url_for('login.login', next=request.url))
