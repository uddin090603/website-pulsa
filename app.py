from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'secret-key-123'
DATABASE = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pulsa', methods=['GET', 'POST'])
def pulsa():
    if request.method == 'POST':
        nomor = request.form['nomor']
        nominal = request.form['nominal']
        metode = request.form['metode']
        conn = get_db_connection()
        conn.execute('INSERT INTO transaksi (nomor, nominal, metode) VALUES (?, ?, ?)', (nomor, nominal, metode))
        conn.commit()
        conn.close()
        return "Pembelian berhasil!"
    return render_template('pulsa.html')

@app.route('/paket-data', methods=['GET', 'POST'])
def paket_data():
    if request.method == 'POST':
        nomor = request.form['nomor']
        provider = request.form['provider']
        paket = request.form['paket']
        conn = get_db_connection()
        conn.execute('INSERT INTO paket_data (nomor, provider, paket) VALUES (?, ?, ?)', (nomor, provider, paket))
        conn.commit()
        conn.close()
        return "Pembelian paket data berhasil!"
    return render_template('paket_data.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']
        if user == 'admin' and pwd == 'admin123':
            session['user'] = user
            return redirect(url_for('riwayat'))
        else:
            return "Login gagal"
    return render_template('login.html')

@app.route('/riwayat')
def riwayat():
    if 'user' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    transaksi = conn.execute('SELECT * FROM transaksi').fetchall()
    conn.close()
    return render_template('riwayat.html', transaksi=transaksi)

@app.route('/riwayat-paket')
def riwayat_paket():
    if 'user' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    riwayat = conn.execute('SELECT * FROM paket_data ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('riwayat.html', riwayat=riwayat)

if __name__ == '__main__':
    conn = get_db_connection()

    conn.execute(
        "CREATE TABLE IF NOT EXISTS paket_data ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "nomor TEXT,"
        "provider TEXT,"
        "paket TEXT)"
    )

    conn.execute(
        "CREATE TABLE IF NOT EXISTS transaksi ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "nomor TEXT,"
        "nominal TEXT,"
        "metode TEXT)"
    )

    conn.commit()
    conn.close()
    app.run(debug=True)
