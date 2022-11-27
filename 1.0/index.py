from flask import Flask, request, render_template, redirect
import sqlite3
import os

app = Flask(__name__, template_folder=os.getcwd() + "\\simple front")


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
        if request.form.get("nick"):
            nick, password, confirm = request.form.values()
            if password !=confirm:
                return render_template("reg-and-log.html", log="password != confirm")
            else:
                some
        if request.form.get("log_name"):
            log_name, log_pass = request.form.values()
            return f'''log in name->{log_name},pass->log_pass'''           
    return render_template("reg-and-log.html")


app.run()
