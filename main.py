# coding:utf8

from flask import Flask, render_template, request, url_for, redirect
from modules import conf, user, message

app = Flask(__name__)


@app.route("/")
def index():
    return "welcome to home."


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone = request.form["phone"]
        password = request.form["password"]
        user_auth = user.User()
        result = user_auth.user_login(phone=phone, password=password)
        if result["code"] == 0:  # rewrite index html
            return redirect("/")
        else:  # rewrite error html
            return str(result["message"])
    return render_template("login.html")


@app.route("/login_message", methods=['GET', 'POST'])
def login_message():
    # 1、如果提交了手机号和验证码
    # 2、如果验证码错误
    result = {}
    if request.method == 'POST':
        phone = request.form["phone"]
        code = request.form["code"]
        if phone:  # 1、手机号为真
            user_auth = user.User()
            if user_auth.phone_check(phone=phone):  # 手机号合法吗？
                if user_auth.user_esxits_status(phone=phone)["code"] == 5:  # 手机号存在数据库
                    if code:  # 验证码为真
                        result_code = user_auth.user_message_login(phone=phone, code=code)  # 验证码验证过程
                        if result_code["code"] == 0:
                            return redirect("/")  # 验证成功，进行跳转
                        else:  # 跳回去告诉验证码失败
                            return render_template("login_message.html",
                                                   result={"data": {"status": 4,}, "message": "验证码失效，请重新发送"})
                    else:  # 验证码为假
                        send_message = message.Message()
                        result_message = send_message.login_code(phone=phone, time=60)  # 发送验证码
                        if result_message["code"] == 0:
                            result = conf._code[0]
                            result["message"] = "验证码短信发送成功"
                            result["data"] = {"status": 0}  # 发送成功
                        else:
                            result = conf._code[201]
                            result["data"] = {"status": 1, "message": "验证码发送失败，请重新发送"}  # 发送失败
                        return render_template("login_message.html", result=result)
                else:
                    result = conf._code[7]
                    result["message"] = "用户未注册，不能登陆"
                    return render_template("login_message.html", result=result)
            else:
                result = conf._code[2]
                result["message"] = "手机号不合法"
                return render_template("login_message.html", result=result)
        else:  # 手机号为假
            return render_template("login_message.html", result=result)
    return render_template("login_message.html", result=result)


@app.route("/reg", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        phone = request.form["phone"]
        password = request.form["password"]
        username = request.form["username"]
        ensure_password = request.form["ensure_password"]
        stage_class = request.form["stage_class"]
        user_reg = user.User()
        result = user_reg.user_reg(phone=phone,
                                   username=username,
                                   password=password,
                                   ensure_password=ensure_password,
                                   stage_class=stage_class)
        if result["code"] == 0:
            return redirect("/")
        else:
            return str(result["message"])
    return render_template("register.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)
