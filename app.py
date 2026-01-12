import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
DB_NAME = 'admin.db'

def connectdb():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = connectdb()
    conn.execute('''CREATE TABLE IF NOT EXISTS surat (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    surat VARCHAR(100) NOT NULL,
                    pengirim VARCHAR(100) NOT NULL,
                    penerima VARCHAR(100) NOT NULL, 
                    nomor_surat VARCHAR(100),
                    tanggal INTEGER
                    )''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = connectdb()
    surat = conn.execute('SELECT * FROM surat ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('index.html', surat=surat)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        surat = request.form['surat']
        pengirim = request.form['pengirim']
        penerima = request.form['penerima']
        nomor_surat = request.form['nomor_surat']
        tanggal = request.form.get('tanggal', None)
        
        conn = connectdb()
        conn.execute('INSERT INTO surat (surat,pengirim,penerima,nomor_surat,tanggal) VALUES (?,?,?, ?, ?)', 
                     (surat,pengirim,penerima,nomor_surat,tanggal))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):     
    conn = connectdb()
    surat = conn.execute('SELECT * FROM surat WHERE id = ?', (id,)).fetchone()
    if not surat:
        conn.close()
        return "Surat Tidak Ditemukan", 404
    
    if request.method == 'POST':
        surat = request.form['surat']
        pengirim = request.form['pengirim']
        penerima = request.form['penerima']
        nomor_surat = request.form['nomor_surat']
        tanggal = request.form.get('tanggal', None)
        
        conn.execute('UPDATE  surat set surat = ?, pengirim = ?, penerima = ?,nomor_surat = ?, tanggal = ? where id = ?',
                     (surat,pengirim,penerima,nomor_surat,tanggal,id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    conn.close()
    return render_template('edit.html', surat=surat)

@app.route('/delete/<int:id>')
def delete(id):
    conn = connectdb()
    conn.execute('DELETE FROM surat WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=6004, debug=True)