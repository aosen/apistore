# -*- coding: utf-8 -*-

import time

from basemodel import BaseModel
import utils

class UserAuthModel(BaseModel):
    def __init__(self):
        super(UserAuthModel, self).__init__()

    def haveUserName(self, appid, username):
        """
        检测用户是否已经存在
        :param appid:
        :param username:
        :return: 如果存在返回True 否则返回 False
        """
        sql = "SELECT username from userinfo WHERE appid_id=%s AND username=%s"
        username = self.db.get(sql, int(appid), username)
        if username:
            return True
        else:
            return False

    def saveUserInfo(self, appid, username, password):
        """
        将用户注册信息入库
        :param appid:
        :param username:
        :param password:
        :return: 保存成功返回True : False
        """
        sql = """
            BEGIN;
            INSERT INTO userinfo (appid_id, username, createtime, updatetime) VALUES (%s, %s, %s, %s);
            INSERT INTO localauth (userid_id, password) VALUES (%s, %s);
            COMMIT;
        """
        insert_userinfo = "INSERT INTO userinfo (appid_id, username, createtime, updatetime) VALUES (%s, %s, %s, %s)"
        insert_localauth = "INSERT INTO localauth (userid_id, password) VALUES (%s, %s)"
        now = str(int(time.time()))
        try:
            userid_id = self.db.insert(insert_userinfo, appid, username, now, now)
        except Exception as e:
            return False
        else:
            try:
                self.db.insert(insert_localauth, userid_id, utils.encodePassword(password))
            except Exception as e:
                return False
        return True