from flask import Flask, request, render_template, redirect
import sqlite3
import os
import string, random

app = Flask(__name__, template_folder=os.getcwd() + "\\simple front")

list()


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
        "SELECT * FROM data WHERE login = ? and password = ?;", (nick, password))
    if is_registry(nick) is False:
        return "login is incorrect"

    if data == "None":
        return "login is incorrect"
    else:
        return "accepted"


def write_bd(nick, password):
    connection = sqlite3.connect("database.sqlite")
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO data(`login`,`password`) VALUES (?, ?)", (nick, password))
    connection.commit()
    return None


def write_post(nick, text, tegs):
    connection = sqlite3.connect("posts.sqlite")
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO data (`autor`, `text`,`tegs`) VALUES (?, ?, ?)", (nick, text, tegs))
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
def get_tegs(tegs):
    return f'''searching tegs : #{tegs}'''


@app.route("/registration_or_autorization", methods=['GET', 'POST'])
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
        if request.form.get("log_name"):  # autorization
            log_name, log_pass = request.form.values()
            log = data_correctly(log_name, log_pass)
            if log != "accepted":
                return render_template("reg-and-log.html", log=log)
            else:
                code = "".join(random.choices(string.digits + string.ascii_lowercase, k=15))
                list.append(code)
                href = str(request.base_url) + "/do/@" + \
                    log_name + "search?code=" + code
                return redirect(href, teg=log_name, auth="auth", code=200)

    return render_template("reg-and-log.html")


@app.route('/do/<nick>/code/', methods=['GET', 'POST'])
def user_obr(nick):
    code = request.args.get('code')
    if code in list:
        list.remove(list.index(code))
        return render_template("blog_page.html", teg=nick)
    else:
        return redirect(str(request.base_url) + "/registration_or_autorization", code=200)
    if request.form.get("post_text"):
        text = request.form.get("post_text")
        tegs = request.form.get("tegs")
        write_post(nick, text, tegs)
        return render_template("blog_page.html", teg=nick, auth="auth")


app.run()
