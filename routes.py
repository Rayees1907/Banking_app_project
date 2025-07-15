from flask import render_template, request, redirect, url_for, session, flash
from .models import create_user, get_user_by_username, check_password, update_user_balance

def init_app_routes(app):

    @app.route('/')
    def index():
        if 'username' in session:
            user = get_user_by_username(session['username'])
            if user:
                return render_template('account.html', user=user)
        return redirect(url_for('login'))

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if not username or not password:
                flash('Username and password are required!', 'error')
                return render_template('register.html')
            if create_user(username, password):
                flash('Account created successfully! Please log in.', 'success')
                return redirect(url_for('login'))
            else:
                flash('Username already exists. Please choose a different one.', 'error')
        return render_template('register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = get_user_by_username(username)
            if user and check_password(user['password'], password):
                session['username'] = user['username']
                session['user_id'] = user['id']
                flash('Logged in successfully!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Invalid username or password.', 'error')
        return render_template('login.html')

    @app.route('/logout')
    def logout():
        session.pop('username', None)
        session.pop('user_id', None)
        flash('You have been logged out.', 'info')
        return redirect(url_for('login'))

    @app.route('/deposit', methods=['GET', 'POST'])
    def deposit():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        if request.method == 'POST':
            try:
                amount = float(request.form['amount'])
                if amount <= 0:
                    flash('Deposit amount must be positive.', 'error')
                else:
                    update_user_balance(session['user_id'], amount)
                    flash(f'Successfully deposited ${amount:.2f}', 'success')
            except ValueError:
                flash('Invalid amount.', 'error')
        return redirect(url_for('index')) # Redirect back to account page

    @app.route('/withdraw', methods=['GET', 'POST'])
    def withdraw():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        if request.method == 'POST':
            try:
                amount = float(request.form['amount'])
                if amount <= 0:
                    flash('Withdrawal amount must be positive.', 'error')
                else:
                    user = get_user_by_username(session['username'])
                    if user and user['balance'] >= amount:
                        update_user_balance(session['user_id'], -amount)
                        flash(f'Successfully withdrew ${amount:.2f}', 'success')
                    else:
                        flash('Insufficient funds or invalid user.', 'error')
            except ValueError:
                flash('Invalid amount.', 'error')
        return redirect(url_for('index')) # Redirect back to account page

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error.html', message="Page Not Found"), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('error.html', message="Internal Server Error"), 500