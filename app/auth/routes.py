# auth/routes.py
from flask import render_template, request, redirect, url_for, flash, session
from . import auth_blueprint
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from supabase import create_client, Client
import os
from dotenv import load_dotenv
load_dotenv()

url: str = os.getenv('SUPABASE_URL')
key: str = os.getenv('SUPABASE_KEY')
supabase: Client = create_client(url, key)


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user_data = supabase.table('users').select('*').eq('username', username).execute()

        if user_data.data and check_password_hash(user_data.data[0]['password_hash'], password):
            session['user_id'] = user_data.data[0]['id']  
            flash('Logged in successfully.')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid username or password.')
            return redirect(url_for('auth.login'))

    return render_template('auth/login.html')

@auth_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        status_page_name = request.form['status_page_name']

        if password != confirm_password:
            flash('Passwords do not match.')
            return redirect(url_for('auth.signup'))
        
        password_hash = generate_password_hash(password)

        data = {
            'username': username,
            'email': email,
            'password_hash': password_hash,
            'status_page_name': status_page_name
        }
        
        inserted_data = supabase.table('users').insert(data).execute()

        # Check if there was an error inserting the data - getting errors for the following line 
        #NOTE - need to fix this as im not sure about the error for supaabse databases
        # if inserted_data['error']:
        #     flash(inserted_data['error'])
        #     return redirect(url_for('auth.signup'))

        flash('Account created successfully, please log in.')
        return redirect(url_for('auth.login'))

    return render_template('auth/signup.html')
