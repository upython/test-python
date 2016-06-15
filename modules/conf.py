# coding:utf8

# db info
db_user = "yhg"
db_password = "123456"
db_host = "188.188.1.113"
db_port = 3306
db_name = "jfpython"
db_charset = "utf8"

# redis info
redis_host = "188.188.0.113"
redis_port = 6379

# message center info
smsbao_username = "zwhset"
smsbao_password = "c6ce77ffe69dc393c38a7788c39a94ca"

'''
#1-100 user login reg error
#101-200 db error
'''
_code = {
    0: {"code": 0, "message": "success"},
    1: {"code": 1, "message": "please you give a post method"},
    2: {"code": 2, "message": "user or password error"},
    3: {"code": 3, "message": "The two passwords do not match"},
    4: {"code": 4, "message": "please you change you phone number"},
    5: {"code": 5, "message": "号码已存在"},
    6: {"code": 6, "message": "号码不存在"},
    7: {"code": 7, "message": "用户未激活"},
    8: {"code": 8, "message": "短信验证码出错"},
    9: {"code": 9, "message": "验证码无值，请重新发送"},
    101: {"code": 101, "message": "db connection error"},
    103: {"code": 103, "message": "db query error"},
    201: {"code": 201, "message": "短信发送失败"},
    202: {"code": 202, "message": "群发短信发送失败"},
    301: {"code": 301, "message": "redis连接失败"},
    302: {"code": 302, "message": "redis 没有此key"},
    303: {"code": 303, "message": "redis set key 错误"},
    304: {"code": 304, "message": "redis 设置超时时间错误"}
}
