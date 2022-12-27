from flask import Flask, request, render_template, redirect, make_response
from threading import Thread
import sqlite3
import os
import string, random
import requests

app = Flask(__name__, template_folder=os.getcwd() + "\\simple front")


def is_registry(nick):
    connection = sqlite3.connect("database.sqlite")
    cursor = connection.cursor()
    data = cursor.execute(
        "SELECT * FROM data WHERE login = (?)", (nick,)).fetchone()
    if data is None:
        return False
    else:
        return True


def data_correctly(nick, password):
    connection = sqlite3.connect("database.sqlite")
    cursor = connection.cursor()
    data = cursor.execute(
        "SELECT * FROM data WHERE login = ? and password = ?;", (nick, password)).fetchone()
    if is_registry(nick) is False:
        return -1
    elif data is None:
        return 1
    else:
        return 0


def write_bd_code(login, code):
    connection = sqlite3.connect("database.sqlite")
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE data SET code = (?) WHERE login = (?)", (code, login))
    connection.commit()
    return None


def check_bd_code(login, code):
    connection = sqlite3.connect("database.sqlite")
    cursor = connection.cursor()
    data = cursor.execute(
        "SELECT * FROM data WHERE login = ? and code = ?", (login, code)).fetchone()
    if data is None:
        return False
    else:
        write_bd_code(login, "")  # clear old 'code'
        return True


def write_bd(nick, password):
    connection = sqlite3.connect("database.sqlite")
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO data(`login`,`password`) VALUES (?, ?)", (nick, password))
    connection.commit()
    return None


def write_post(nick, text, tags):
    connection = sqlite3.connect("posts.sqlite")
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO data (`autor`, `text`,`tegs`) VALUES (?, ?, ?)", (nick, text, tags))
    connection.commit()
    return None


@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("Main_page.html")


@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        if request.form.get("username"):
            nick = request.form.get("username")
            href_to = str(request.base_url) + "/acc/@" + str(nick)
            return redirect(href_to, code=302)

        if request.form.get("postteg"):
            teg = request.form.get("postteg")
            href = str(request.base_url) + "/tegs/" + str(teg)
            return redirect(href, code=302)

    return render_template("search.html")


@app.route('/search/acc/@<id>')
def get_acc(id):
    return f'''searching @{id}'''


@app.route('/search/tegs/<tegs>')
def get_tags(tags):
    return f'''searching tags : #{tags}'''


@app.route("/registration_or_authorization", methods=['GET', 'POST'])
def reg_and_log():
    if request.method == "POST":
        if request.form.get("nick"):  # registration
            nick, password, confirm = request.form.values()
            if password != confirm:
                return render_template("reg-and-log.html",
                                       log="password != confirm")
            else:
                if is_registry(nick):
                    return render_template("reg-and-log.html",
                                           log="already is")
                else:
                    write_bd(nick, password)
                    return render_template("reg-and-log.html",
                                           log="accepted")

        # - - - - - - - - - - - - - - - - - - - - - - - - - #

        if request.form.get("log_name"):  # authorization
            log_name, log_pass = request.form.values()
            log = data_correctly(log_name, log_pass)
            if log == -1:
                return render_template("reg-and-log.html", log="This account was not registered")
            if log == 1:
                return render_template("reg-and-log.html", log="Password incorrectly")
            else:
                code = "".join(random.choices(string.digits + string.ascii_lowercase, k=15))
                write_bd_code(log_name, code)
                res = make_response(redirect("blog/me/"+log_name, code=302))
                res.set_cookie('code', code, 3600)
                return res

    return render_template("reg-and-log.html")


@app.route('/blog/me/<nick>', methods=['GET', 'POST'])
def user_handler(nick):
    code = request.cookies.get('code')
    if check_bd_code(nick, code):
        return render_template("blog_page.html")
    else:
        return redirect("/registration_or_authorization?auth=false&error=code_not_in_list",code=302)


app.run()
