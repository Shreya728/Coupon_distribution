from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, g
import sqlite3
import os
from datetime import datetime, timedelta
import secrets
import functools
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
DATABASE = 'database.db'

def get_db_connection():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE, check_same_thread=False)
        db.row_factory = sqlite3.Row
    return db

def initialize_database():
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        conn.executescript('''
            CREATE TABLE coupons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code VARCHAR(50) UNIQUE NOT NULL,
                is_active BOOLEAN DEFAULT 1,
                claimed_by_ip VARCHAR(45),
                claimed_by_session VARCHAR(32),
                claimed_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE admins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(80) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL
            );
        ''')
        hashed_pw = generate_password_hash('shreya123')
        conn.execute('INSERT INTO admins (username, password) VALUES (?, ?)', ('Shreya', hashed_pw))
        conn.commit()
        conn.close()
        print("✅ New database initialized!")

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        return view(**kwargs)
    return wrapped_view

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/claim_coupon', methods=['POST'])
def claim_coupon():
    ip_address = request.remote_addr
    session_id = session.get('user_session', None)
    
    if not session_id:
        session_id = secrets.token_hex(16)
        session['user_session'] = session_id
    
    conn = get_db_connection()
    user_claim = conn.execute(
        'SELECT claimed_at FROM coupons WHERE claimed_by_ip = ? OR claimed_by_session = ?',
        (ip_address, session_id)
    ).fetchone()
    
    if user_claim and user_claim['claimed_at']:
        claimed_time = datetime.fromisoformat(user_claim['claimed_at'])
        cooldown_end = claimed_time + timedelta(hours=24)
        now = datetime.now()
        
        if now < cooldown_end:
            hours_left = int((cooldown_end - now).total_seconds() / 3600)
            return jsonify({'success': False, 'message': f'You can claim another coupon in {hours_left} hours.'})
    
    coupon = conn.execute('SELECT id, code FROM coupons WHERE is_active = 1 AND claimed_by_ip IS NULL ORDER BY id LIMIT 1').fetchone()
    
    if not coupon:
        return jsonify({'success': False, 'message': 'Sorry, no coupons available at the moment.'})
    
    now = datetime.now().isoformat()
    conn.execute(
        'UPDATE coupons SET claimed_by_ip = ?, claimed_by_session = ?, claimed_at = ? WHERE id = ?',
        (ip_address, session_id, now, coupon['id'])
    )
    conn.commit()
    return jsonify({'success': True, 'message': 'Coupon claimed successfully!', 'coupon_code': coupon['code']})

@app.route('/admin')
def admin_login():
    return render_template('admin_login.html')

@app.route('/admin/login', methods=['POST'])
def admin_login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    
    conn = get_db_connection()
    admin = conn.execute('SELECT * FROM admins WHERE username = ?', (username,)).fetchone()
    
    if admin and check_password_hash(admin['password'], password):
        session['admin_logged_in'] = True
        return redirect(url_for('admin_panel'))
    
    flash('Invalid credentials')
    return redirect(url_for('admin_login'))

@app.route('/admin/panel')
@admin_required
def admin_panel():
    conn = get_db_connection()
    coupons = conn.execute('SELECT * FROM coupons ORDER BY id').fetchall()
    return render_template('admin_panel.html', coupons=coupons)

@app.route('/admin/add_coupon', methods=['POST'])
@admin_required
def add_coupon():
    code = request.form.get('code')
    
    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO coupons (code, is_active) VALUES (?, 1)', (code,))
        conn.commit()
        flash('Coupon added successfully')
    except sqlite3.IntegrityError:
        flash('Coupon code must be unique!')
    
    return redirect(url_for('admin_panel'))

@app.route('/admin/toggle_coupon/<int:id>', methods=['POST'])
@admin_required
def toggle_coupon(id):
    conn = get_db_connection()
    coupon = conn.execute('SELECT is_active FROM coupons WHERE id = ?', (id,)).fetchone()
    
    if coupon:
        new_status = 0 if coupon['is_active'] == 1 else 1
        conn.execute('UPDATE coupons SET is_active = ? WHERE id = ?', (new_status, id))
        conn.commit()
    
    return redirect(url_for('admin_panel'))

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

if __name__ == '__main__':
    initialize_database()
    app.run(debug=True)