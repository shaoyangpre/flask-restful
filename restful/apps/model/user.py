from sqlalchemy import Column, String, Integer, orm, Text, DateTime
from werkzeug.security import check_password_hash,generate_password_hash

from .import Base,db
from apps.libs.error_code import NotFound, AuthFailed


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)  # 编号
    name = Column(String(100), unique=True)  # 昵称
    _pwd = Column('pwd', String(100))  # 密码
    email = Column(String(100), unique=True)  # 邮箱
    phone = Column(String(11), unique=True)  # 电话号码
    info = Column(Text)  # 个性简介
    face = Column(String(255), unique=True)  # 头像
    uuid = Column(String(255), unique=True)  # 唯一标志符

    def keys(self):
        return ['id', 'email', 'nickname', 'auth']

    @property
    def pwd(self):
        return self._pwd

    @pwd.setter
    def pwd(self, raw):
        self._pwd = generate_password_hash(raw)

    @staticmethod
    def register_by_email(name, account, secret):
        with db.auto_commit():
            user = User()
            user.name = name
            user.email = account
            user.pwd = secret
            db.session.add(user)

    @staticmethod
    def verify(email, password):
        user = User.query.filter_by(email=email).first_or_404()
        if not user.check_pwd(password):
            raise AuthFailed()
        # scope = 'AdminScope' if user.auth == 2 else 'UserScope'
        return {'uid': user.id, 'scope': 'AdminScope'}

    def check_pwd(self, pwd):
        return check_password_hash(self.pwd, pwd)