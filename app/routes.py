from flask import Blueprint, render_template, session, redirect, url_for, flash
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

url: str = os.getenv('SUPABASE_URL')
key: str = os.getenv('SUPABASE_KEY')
supabase: Client = create_client(url, key)

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home/index.html')

@main.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    user_data = supabase.table('users').select('username', 'status_page_name').eq('id', user_id).execute()

    if user_data.data:
        username = user_data.data[0]['username']
        status_page_name = user_data.data[0]['status_page_name']
        return render_template('_dash/dashboard.html', username=username, status_page_name=status_page_name)
    else:
        flash('User not found.')
        return redirect(url_for('auth.login'))

