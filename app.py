from flask import Flask, render_template, redirect, url_for, request
import pymysql

app = Flask(__name__)

db_conn = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    db='info_db',
    cursorclass=pymysql.cursors.DictCursor
)


# @app.route('/dbcheck')
# def dbcheck():
#     if db_conn.open:
#         return '<h1 style="color:green;">Connected</h1>'
#     else:
#         return '<h1 style="color:red;">Not Connected</h1>'


#Index
@app.route('/')
def index():
    cursor = db_conn.cursor()
    cursor.execute('SELECT * FROM tbl_info')
    info = cursor.fetchall()
    cursor.close()
    return render_template('index.html', infos=info)

#Add
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        cursor = db_conn.cursor()
        fname = request.form['fname']
        contact = request.form['contact']
        email_add = request.form['email_add']
        cursor.execute('INSERT INTO tbl_info (fname, contact, email_add) VALUES (%s, %s, %s)', (fname, contact, email_add))
        db_conn.commit()
        cursor.close()
        return redirect(url_for('index'))
    return render_template('add.html')

#Delete
@app.route('/delete/<int:info_id>')
def delete(info_id):
    cursor = db_conn.cursor()
    cursor.execute('DELETE FROM tbl_info WHERE info_id=%s', (info_id))
    cursor.close()
    db_conn.commit()
    return redirect(url_for('index'))

#Edit
@app.route('/edit/<int:info_id>', methods=['GET', 'POST'])
def edit(info_id):
    cursor = db_conn.cursor()
    cursor.execute('SELECT * FROM tbl_info WHERE info_id=%s', (info_id))
    info = cursor.fetchone()
    cursor.close()
    if request.method == 'POST':
        cursor = db_conn.cursor()
        fname = request.form['fname']
        contact = request.form['contact']
        email_add = request.form['email_add']
        cursor.execute('UPDATE tbl_info SET fname=%s, contact=%s, email_add=%s WHERE info_id=%s', (fname, contact, email_add, info_id))
        db_conn.commit()
        cursor.close()
        return redirect(url_for('index'))
    return render_template('edit.html', info=info)

if __name__ == '__main__':
    app.run(debug=True)