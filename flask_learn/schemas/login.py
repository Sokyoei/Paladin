from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(FlaskForm):
    email = StringField(
        '邮箱', validators=[DataRequired(message="邮箱不能为空"), Email(message="请输入有效的邮箱地址")]
    )
    password = PasswordField(
        '密码', validators=[DataRequired(message="密码不能为空"), Length(min=6, message="密码至少6位")]
    )
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')


class RegisterForm(FlaskForm):
    username = StringField(
        '用户名', validators=[DataRequired(message="用户名不能为空"), Length(min=3, max=64, message="用户名长度3-64位")]
    )
    email = StringField(
        '邮箱', validators=[DataRequired(message="邮箱不能为空"), Email(message="请输入有效的邮箱地址")]
    )
    password = PasswordField(
        '密码', validators=[DataRequired(message="密码不能为空"), Length(min=6, message="密码至少6位")]
    )
    confirm_password = PasswordField('确认密码', validators=[DataRequired(message="请确认密码")])
    submit = SubmitField('注册')
