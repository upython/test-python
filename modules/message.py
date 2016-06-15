# coding:utf8
import requests
import redis
import conf
import sys
import db
import random

reload(sys)
sys.setdefaultencoding("utf8")


class Message:
    def __init__(self):
        self.smsbao_url = "http://api.smsbao.com/sms"

    def smsbao_message(self, phone, content):
        try:
            # http://api.smsbao.com/sms?u=USERNAME&p=PASSWORD&m=PHONE&c=CONTENT
            payload = {
                "u": conf.smsbao_username,  # username
                "p": conf.smsbao_password,  # password
                "m": phone,  # phone
                "c": content  # content
            }
            message_code = {
                "0": "发送成功",
                "30": "密码错误",
                "40": "账号不存在",
                "41": "余额不足",
                "42": "帐号过期",
                "43": "IP地址限制",
                "50": "内容含有敏感词",
                "51": "手机号码不正确",
                "-1": "参数不全"
            }
            r = requests.get(self.smsbao_url, params=payload)
            result_code = r.text
            if result_code == "0":  # 如果发送成功
                result = conf._code[0]
                result["message"] = "发送成功"
                return result
            else:  # 发送失败改写message
                result = conf._code[201]
                result["message"] = message_code[result_code]
                return result
        except Exception, e:
            result = conf._code[201]
            result["message"] = e
            return result

    # 课堂上课通知
    def class_notice(self, time="20:00", clas="python"):

        db_result = db.SQLdb()
        db_result = db_result.get_connection()
        if db_result:
            conn, cursor = db_result
            query = "SELECT phone,username FROM jf_user"
            try:
                cursor.execute(query)
                data = cursor.fetchall()
                for phone, username in data:
                    content = "【京峰课堂】尊敬的{username}:我们将于晚上{time}进行{clas}上课，请准时上课。".format(username=username,
                                                                                         time=time,
                                                                                         clas=clas)
                    print phone, username
                    print self.smsbao_message(phone, content)
            except Exception, e:
                result = conf._code[202]
                return result
        else:
            result = conf._code[101]
            return result

    def login_code(self, phone, time=60):
        # 1 获取4位随机验证码
        code = random.randint(1000, 9999)

        # 2 发送到redis并设置失效时间
        try:
            redis_conn = redis.StrictRedis(host=conf.redis_host,
                                           port=conf.redis_port)
            try:
                redis_conn.set(name=phone, value=code)
                redis_conn.expire(name=phone, time=time)

                content = "【京峰课堂】您的验证码为{code}，在{time}秒内有效。".format(code=code,
                                                                   time=time)
                result_smsbao = self.smsbao_message(phone=phone, content=content)["code"]
                if result_smsbao == 0:  # 发送短信给客户
                    result = conf._code[0]
                    result["data"] = {"expire": code}
                    return result
                else:
                    return result_smsbao
            except Exception, e:
                result = conf._code[303]
                result["message"] = e
                return result
        except Exception, e:
            result = conf._code[301]
            result["message"] = e
            return result


if __name__ == "__main__":
    a = Message()
    print a.login_code(phone=18910767815)
