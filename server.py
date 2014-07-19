import sqlite3
import time
import json
import random
import string
from flask import Flask, request, g, render_template, redirect, jsonify
app = Flask(__name__)

DATABASE = 'torMessages.db'

def get_db():
	db = getattr(g, '_database', None)
	if db is None:
		db = g._database = sqlite3.connect(DATABASE)
		c = db.cursor()
		c.execute("CREATE TABLE IF NOT EXISTS messages (message TEXT, sender TEXT, time TEXT)")
		get_db().commit()
	return db

@app.teardown_appcontext
def close_connection(exception):
	db = getattr(g, '_database', None)
	if db is not None:
		db.close()

def db_read_messages():
	cur = get_db().cursor()
	cur.execute("SELECT * FROM messages ORDER BY time DESC LIMIT 20")
	return cur.fetchall()

def db_add_message(message, sender):
	cur = get_db().cursor()
	t = str(time.time())
	cur.execute("INSERT INTO messages VALUES (?, ?, ?)", (message, sender, t))
	get_db().commit()

@app.route("/")
def hello():
	return render_template('index.html', sender=''.join(random.choice(string.ascii_lowercase) for _ in range(5)))

@app.route("/api/send", methods=["POST"])
def receive_message():
	db_add_message(request.form['message'], request.form['sender'])
	return redirect("/")

@app.route("/api/messages")
def get_messages():
	return json.dumps(db_read_messages())

if __name__ == "__main__":
	app.run(debug=True)

# import sqlite3
# import time
# from flask import Flask, g, request, render_template, redirect

# app = Flask(__name__)
# DATABASE = 'cheeps.db'

# def get_db():
#     db = getattr(g, '_database', None)
#     if db is None:
#         db = g._database = sqlite3.connect(DATABASE)
#     return db

# @app.teardown_appcontext
# def close_connection(exception):
#     db = getattr(g, '_database', None)
#     if db is not None:
#         db.close()

# def db_read_cheeps():
#     cur = get_db().cursor()
#     cur.execute("SELECT * FROM cheeps")
#     return cur.fetchall()

# def db_add_cheep(name, cheep):
#     cur = get_db().cursor()
#     t = str(time.time())
#     cheep_info = (name, t, cheep)
#     cur.execute("INSERT INTO cheeps VALUES (?, ?, ?)", cheep_info)
#     get_db().commit()

# @app.route("/")
# def hello():
#     cheeps = db_read_cheeps()
#     print(cheeps)
#     return render_template('index.html', cheeps=cheeps)

# @app.route("/api/cheep", methods=["POST"])
# def receive_cheep():
#     print(request.form)
#     db_add_cheep(request.form['name'], request.form['cheep'])
#     return redirect("/")

# if __name__ == "__main__":
#     app.run()
