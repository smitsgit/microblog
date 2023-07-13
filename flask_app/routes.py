from flask import render_template, flash, redirect, url_for

from flask_app import app
from flask_app.forms import LoginForm


@app.route("/")
@app.route("/index")
def index():
    mock_user = {'username': 'Smital'}
    mock_posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("index.html", title="smital", user=mock_user, posts=mock_posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        flash(f"Login requested for {login_form.username.data}, remember_me={login_form.remember_me.data}")
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=login_form)
