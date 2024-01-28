from . import auth_blueprint
from flask import render_template

@auth_blueprint.route('/login')
def login():
    return render_template('auth/login.html')


