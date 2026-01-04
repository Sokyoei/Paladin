from flask_login import LoginManager

login_manager = LoginManager()
login_manager.login_view = 'login.login'
login_manager.login_message = "请登录"
login_manager.login_message_category = "info"
