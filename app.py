from flask import Flask, request, jsonify, render_template
import sqlite3
import re

app = Flask(__name__)

def init_db():
    with sqlite3.connect('email.db') as conn:
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
    data = request.get_json()
    email = data.get('email')
    if email and re.match(r"[^@]+@[^@]+\.[^@]+", email):
        try:
            with sqlite3.connect('email.db') as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO subscribers (email) VALUES (?)',(email,))
                conn.commit()
            return jsonify({'message': 'Subscrption Success!'}),200
        
        except sqlite3.IntegrityError:
            return jsonify({'message': 'email already subscribed'}),409

    return jsonify({'message':'invalid email'}),400
        
if __name__ == '__main__':
    init_db()
    app.run(debug=False)
