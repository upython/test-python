# coding:utf8
import redis
import conf


class Redis:
    def __init__(self):
        pass

    def get_redis(self):
        try:
            redis_conn = redis.StrictRedis(host="192.168.100.8", port=6379)
            result = conf._code[0]
            result["data"] = redis_conn
            return result
        except Exception, e:
            result = conf._code[301]
            return result

    def get(self, name):
        try:
            redis_conn = get_redis()
            value = redis_conn.get(name)
            if value:
                result = conf._code[0]
                result["data"] = {"value": value}
                return reslut
            else:
                result = conf._code[302]
                return result
        except Exception, e:
            result = conf._code[301]
            return result

    def set(self, name, value):
        try:
            redis_conn = get_redis()
            redis_conn.set(name, value)
            result = conf._code[0]
            result["data"] = {"value": value}
            return reslut
        except Exception, e:
            result = conf._code[301]
            return result

    def expire(self, name, time):
        try:
            redis_conn = get_redis()
            redis_conn.expire(name, time)
            result = conf._code[0]
            result["message"] = "redis key失效时间设置成功"
            return result
        except Exception, e:
            result = conf._code[301]
            return result
