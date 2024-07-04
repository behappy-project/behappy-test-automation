#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2024/4/25
# @File    : sqlalchemy_mysql_tool.py
# @Software: IntelliJ IDEA

__author__ = 'xiaowu'

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker


class SQLAlchemy_Mysql_Tool:
    def __init__(self, host: str = None, port: str = None, username: str = None, password: str = None, db: str = None,
                 driver_type='pymysql', encoding='utf8', echo=False) -> None:
        self.url = 'mysql+%s://%s:%s@%s:%s/%s' % (driver_type, username, password, host, str(port), db)
        self.encoding = encoding
        self.echo = echo

    def get_session(self):
        engine = create_engine(url=self.url, encoding=self.encoding, echo=self.echo)
        # 线程安全
        return scoped_session(sessionmaker(bind=engine))
