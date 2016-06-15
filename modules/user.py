#coding:utf8

import conf
import db
import hashlib
import sys
import redis
reload(sys)
sys.setdefaultencoding("utf8")

class User:
    def __init__(self):
        pass

    def user_esxits_status(self,phone):#验证用户是否存在和激活
        user = db.SQLdb()
        db_result = user.get_connection()
        if db_result:
            conn,cursor = db_result
            query = 'SELECT status FROM jf_user \
                                 WHERE phone="{phone}"'.format(phone=phone)
            if cursor.execute(query):#号码检测
                result = conf._code[5]#存在
                status = cursor.fetchone()[0]
                result["status"]=status
            else:
                result = conf._code[6]#不存在
            result["data"] = conn,cursor
            return result
        else:
            return conf._code[101]

    def phone_check(self,phone):#手机号检测
        if phone.isalnum() and len(phone) == 11: #11 number
            return True
        else:
            return False

    def user_message_login(self,phone,code):
        try:
            redis_conn = redis.StrictRedis(host=conf.redis_host,port=conf.redis_port)
            result = redis_conn.get(phone)
            if result:#redis里有值，不做此会出BUG
                if code == result:#值相等
                    result = conf._code[0]
                    return result
                else:
                    result = conf._code[8]
                    return result
            else:
                result = conf._code[9]
                return result
        except Exception, e:
            result = conf._code[301]
            return result
            
    def user_login(self,phone,password):
        if not self.phone_check:
            return conf._code[4]

        db_result = self.user_esxits_status(phone=phone)
        if db_result["code"] == 5:#号码存在
            if db_result["status"] != 1:
                return conf._code[7]
            conn,cursor = db_result["data"]
            query = 'SELECT password FROM jf_user \
                                 WHERE phone="{phone}"'.format(phone=phone)
            try:          
                if cursor.execute(query):
                    db_password = cursor.fetchone()[0] #(("password"),("password"))
                    cursor.close();conn.close()
                    if db_password == hashlib.md5(password).hexdigest():
                        return conf._code[0]
                    else:
                        return conf._code[2] #password error
                else:
                    cursor.close();conn.close()
                    return conf._code[2] #user esxits
            except Exception, e:
                cursor.close();conn.close()
                result = conf._code[101]
                result["message"]=e
                return result
        else:
            return db_result
    
    def user_reg(self,phone,username,password,ensure_password,stage_class):
        if not self.phone_check(phone):
            return conf._code[4]
            
        if password == ensure_password:
            db_result = self.user_esxits_status(phone=phone)
            if db_result["code"] == 6:
                conn,cursor = db_result["data"]
                query = 'INSERT INTO jf_user(phone,username,password,stage_class) \
                            VALUES("{phone}","{username}",md5("{password}"),"{stage_class}")'.format(phone=phone,
                                                                                     username=username,
                                                                                     password=password,
                                                                                     stage_class=stage_class)
                try:
                    cursor.execute(query)
                    conn.commit()
                    cursor.close();conn.close()
                    return conf._code[0]
                except Exception, e:
                    cursor.close();conn.close()
                    result = conf._code[101]
                    result["message"] = e
                    return result
            else:
                return db_result
        else:
            return conf._code[3]

    

