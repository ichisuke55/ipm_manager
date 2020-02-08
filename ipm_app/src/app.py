import logging
from flask import Flask, render_template, request, url_for, redirect, flash, session
import MySQLdb

app = Flask(__name__)
app.secret_key = 'session_key'
logging.basicConfig(format="%(asctime)s [%(levelname)s] %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

db_setting = {
    "host": "172.17.0.2",
    "user": "root",
    "passwd": "Ichi2116",
    "db": "ipm_database",
    "charset": "utf8mb4"
    }

def db_connect(db_setting):
    try:
        db_conn = MySQLdb.connect(**db_setting)
    except Exception as e:
        logger.error("%s %s", type(e), e)
    return db_conn


def db_get(db_setting):
    data = []
    db_conn = db_connect(db_setting)
    try:
        cursor = db_conn.cursor()
        query = "SELECT * FROM ipm_table ORDER BY INET_ATON(ip_address)"
        cursor.execute(query)
        data = cursor.fetchall()
        db_close(db_conn)
    except Exception as e:
        logger.error("%s %s", type(e), e)
    return data


def db_close(db_conn):
    db_conn.close()


def db_add(ip_address, host_name, notes):
    db_conn = db_connect(db_setting)
    try:
        cursor = db_conn.cursor()
        cursor.execute(f"INSERT INTO ipm_table (ip_address, hostname, note) VALUES ('{ip_address}', '{host_name}', '{notes}')")
        db_conn.commit()
    except Exception as e:
        logger.error("%s %s", type(e), e)


@app.route('/')
def top():
    data = db_get(db_setting)
    return render_template('top.html', data=data)


@app.route('/add_node', methods=['GET', 'POST'])
def add_node():
    ip_address = request.form["formIpAddress"]
    host_name = request.form["formHostName"]
    notes = request.form["formNotes"]
    db_add(ip_address, host_name, notes)

    return render_template('add_node.html')


@app.route('/delete_node/<node_ip>', methods=['GET', 'POST'])
def delete_node(node_ip):
    if request.method == 'GET':
        return render_template('delete_node.html', node_ip=node_ip)
    
    db = db_connect(db_setting)
    cursor = db.cursor()
    cursor.execute(f'DELETE FROM ipm_table WHERE ip_address = "{node_ip}"')
    db.commit()
    db_close(db)

    flash('対象Hostが削除されました。', category='alert alert-info')
    return redirect(url_for('top'))


@app.route('/edit_node', methods=['GET', 'POST'])
def edit_node(node):
    if request.method == 'GET':
        return render_template('edit_node.html', )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
