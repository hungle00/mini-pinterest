from flask import Flask, redirect, url_for, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from oauth import OAuthSignIn

from models import db, User, Pin


app = Flask(__name__)
app.config['SECRET_KEY'] = 'top secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['OAUTH_CREDENTIALS'] = {
    'google': {
        'id':'9699437797-n0v534ssokcsv64u4jk9bbn2tounv57s.apps.googleusercontent.com',
        'secret':'9cP5SMe-QPbXarq_rlJwHU9-'
    },
    'twitter': {
        'id':'28whRejVnGyRbLOYrgXveWgJ1',
        'secret':'WMghu6fU7Z7ApNhdW38bISklppHSwwBduxGtNPjmBUj5iWJeEF'
    }
}

db.init_app(app)
db.create_all(app=app)
lm = LoginManager(app)
lm.login_view = 'login'

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

app_name = 'Pinterest Clone'

@app.route('/')
@app.route('/index')
@login_required
def index():
    nickname = current_user.nickname
    images = list(reversed(Pin.query.all()))
    return render_template('grid.html',
            title='All images', app_name=app_name, images=images, user=nickname)


@app.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    return render_template('login.html', app_name = app_name, title='Login')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/auth/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@app.route('/auth/<provider>/authorized')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('index'))
    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        user = User(social_id=social_id, nickname=username, email=email)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
