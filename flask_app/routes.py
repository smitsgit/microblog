from flask import render_template

from flask_app import app


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
