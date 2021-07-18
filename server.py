from flask import Flask, render_template, send_from_directory, request, url_for, redirect, flash
import os

from flask_wtf import FlaskForm, Recaptcha, RecaptchaField, CSRFProtect
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, URL, ValidationError

from loadenv import environ

import sqlite3

import socket

def alphanumericcheck(form, field):
    if not field.data.isalnum():
        raise ValidationError("Must only contain alphabets and numbers")

class TrimForm(FlaskForm):
    longurl = StringField(
        render_kw={"placeholder": "Original URL"},
        validators=[
            URL(message=("Not a valid URL")),
            DataRequired()
        ]
    )
    shorturl = StringField(
        render_kw={"placeholder": "Shortened URL (Optional)"},
        validators=[
            alphanumericcheck,
            DataRequired()
        ]
    )
    trimcaptcha = RecaptchaField(
        validators=[
            Recaptcha(message="Please complete the captcha")
        ]
    )
    trim = SubmitField("Trim")

class ContactForm(FlaskForm):
    email = StringField(
        render_kw={"placeholder": "Email"},
        validators=[
            Email(message=("Invalid email address")),
            DataRequired()
        ]
    )
    message = TextAreaField(
        render_kw={"placeholder": "Message"},
        validators=[
            DataRequired()
        ]
    )
    contactcaptcha = RecaptchaField(
        validators=[
            Recaptcha(message="Please complete the captcha")
        ]
    )
    submit = SubmitField("Send")

def createconnection(dbfile):
    conn = sqlite3.connect(dbfile)
    return conn

def createtable(conn, sql):
    conn.cursor().execute(sql)

def createlink(conn, id, original):
    sql = '''INSERT INTO links(id, original)
             VALUES(?, ?)'''
    if checkfree(conn, id):
        conn.cursor().execute(sql, (id, original))
        conn.commit()
        return True
    return False

def checkfree(conn, value):
    query = '''SELECT id FROM links WHERE id = ?'''
    check = conn.cursor().execute(query, (value,)).fetchall()
    return len(check) == 0

environ()

host = socket.gethostbyname(socket.gethostname())
port = 8080

conn = createconnection("./links.db")

linkstable = """CREATE TABLE IF NOT EXISTS links (
                    id text PRIMARY KEY,
                    original text NOT NULL
                );"""          

createtable(conn, linkstable)

csrf = CSRFProtect()

app = Flask(__name__)
csrf.init_app(app)

app.config["RECAPTCHA_PUBLIC_KEY"] = os.environ["RECAPTCHA_SITE_KEY"]
app.config["RECAPTCHA_PRIVATE_KEY"] = os.environ["RECAPTCHA_SECRET_KEY"]
app.config['SECRET_KEY'] = os.environ["SECRET_KEY"]

@app.route("/", methods=["GET", "POST"])
def home():
    form1 = TrimForm()
    form2 = ContactForm()
    if form1.trim.data and form1.validate_on_submit():
        longurl = form1.longurl.data
        shorturl = form1.shorturl.data
        conn = createconnection("./links.db")
        url = createlink(conn, shorturl, longurl)
        if url:
            flash(shorturl, "trimsuccess")
            return redirect(url_for("home", _anchor="trim"))
        flash("Shortened link is already taken", "trimfailed")
        return redirect(url_for("home", _anchor="trim"))

    if form2.submit.data and form2.validate_on_submit():
        email = form2.email.data
        message = form2.message.data
        print("\nContact Form Received\nEmail: {}\nMessage: {}\n".format(email, message))

        #DO SOMETHING WITH CONTACT DATA
        flash("Message Sent", "contactsuccess")
        return redirect(url_for("home", _anchor="contact"))
    return render_template(
        "index.html",
        form1=form1,
        form2=form2
    )

@app.route("/<path:path>")
def homepath(path):
    conn = createconnection("./links.db")
    if checkfree(conn, path):
        return redirect(url_for("home"))
    else:
        query = '''SELECT original FROM links WHERE id = ?'''
        location = conn.cursor().execute(query, (path,)).fetchall()[0][0]
        return redirect(location)

@app.route("/css/<path:path>")
def css(path):
    return send_from_directory("css", path)

@app.route("/js/<path:path>")
def js(path):
    return send_from_directory("js", path)

@app.route("/static/<path:path>")
def staticpath(path):
    return send_from_directory("static", path)

if __name__ == "__main__":
    app.run(host=host, port=port)