from flask import Flask, request, redirect, render_template # type: ignore
import sqlite3
import re
app = Flask(__name__)

def init_db():
    with sqlite3.conntect('email.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS subscribers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE
            )
        ''')
        conn.commit()


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email')
    if email and re.match(r"[^@]+@[^@]+\.[^@]+", email):
        try:
            with sqlite3.connect('email.db') as conn:
                cursor.conn.cursor()
                cursor.execute('INSERT INTO subscribers (email) VALUES (?)',(email,))
                conn.commit()
            return redirect('/')
        except sqlite3.IntegrityError:
            return "Email already subscribed", 409
        
    return "Invalid email", 400
        
if __name__ == '__main__':
    app.run(debug=False)
