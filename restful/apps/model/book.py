from sqlalchemy import Column, String, Integer, orm, Text, DateTime, SmallInteger, BigInteger, Date

from .import Base

class Movie(Base):
    __tablename__ = "movie"
    id = Column(Integer, primary_key=True)  # 编号
    title = Column(String(255), unique=True)  # 电影标题
    url = Column(String(255), unique=True)  # 电影地址
    info = Column(Text)  # 电影简介
    logo = Column(String(255), unique=True)  # 电影封面
    star = Column(SmallInteger)  # 星级
    playnum = Column(BigInteger)  # 电影播放量
    commentnum = Column(BigInteger)  # 电影评论量
    area = Column(String(255))  # 地区
    release_time = Column(Date)  # 发布时间
    length = Column(String(100))  # 电影长度
