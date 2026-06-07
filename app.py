from flask import Flask, request, jsonify from database import get_db import json, datetime, random, string app = Flask(__name__)
@app.route('/register', methods=['POST']) def register(): d = request.json db = get_db(); c = db.cursor() try:
c.execute("INSERT INTO users(name,email,password)
VALUES(?,?,?)", (d['name'], d['email'], d['password'])) db.commit() return {"msg":"ok"} except:
return {"msg":"exists"}
@app.route('/login', methods=['POST']) def login(): d = request.json db = get_db(); c = db.cursor()
c.execute("SELECT * FROM users WHERE email=? AND
password=?", (d['email'], d['password']))
u = c.fetchone() return {"success":bool(u)}
@app.route('/enroll', methods=['POST']) def enroll(): d = request.json
if int(d['age'])<20 or float(d['cgpa'])<7:
return {"msg":"not eligible"} db = get_db(); c = db.cursor()
c.execute("UPDATE users SET enrolled=1 WHERE email=?", (d['email'],)) db.commit() return {"msg":"enrolled"}
@app.route('/questions', methods=['POST']) def add_q():
d = request.json db = get_db(); c = db.cursor()
c.execute("INSERT INTO questions VALUES(?,?,?,?)",
(d['type'], d['question'], json.dumps(d['options']), d['answer'])) db.commit() return {"msg":"added"} @app.route('/questions/<t>') def get_q(t):
db = get_db(); c = db.cursor()
c.execute("SELECT * FROM questions WHERE module_type=?",
(t,)) return jsonify([dict(r) for r in c.fetchall()])
@app.route('/pay', methods=['POST']) def pay():
d = request.json reg = 'REG-'+''.join(random.choices(string.ascii_uppercase,
k=6)) db = get_db(); c = db.cursor()
c.execute("INSERT INTO payments VALUES(?,?,?,?)",
(d['email'], d['exam'], reg, datetime.datetime.now())) db.commit() return {"regId":reg}
@app.route('/result', methods=['POST']) def result(): d = request.json db = get_db(); c = db.cursor()
c.execute("INSERT INTO results VALUES(?,?,?,?,?,?)",
(d['name'], d['email'], d['type'],
d['score'], d['total'], datetime.datetime.now())) db.commit() return {"msg":"saved"}
app.run() database.py import sqlite3, json def get_db():
return sqlite3.connect("mockify.db") def init_db():
db = get_db(); c = db.cursor()
c.execute("CREATE TABLE IF NOT EXISTS questions(id INTEGER
PRIMARY KEY, type TEXT, question TEXT, options TEXT, answer
INT)")
c.execute("CREATE TABLE IF NOT EXISTS results(id INTEGER PRIMARY KEY, name TEXT, email TEXT, type TEXT, score INT, total INT, date TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS payments(id INTEGER
PRIMARY KEY, email TEXT, exam TEXT, reg TEXT UNIQUE, date
TEXT)")
c.execute("SELECT COUNT(*) FROM questions")
if c.fetchone()[0] == 0: qs = [
("aptitude","2+2=?",["2","4","6","8"],1),
("reasoning","Next: 2,4,6?",["8","10","12","14"],0),
("coding","Stack is?",["FIFO","LIFO","Tree","Graph"],1),
("verbal","Synonym of
Hardworking?",["Lazy","Active","Diligent","Weak"],2)] for t,q,o,a in qs:
c.execute("INSERT INTO questions(type,question,options,answer) VALUES(?,?,?,?)", (t,q,json.dumps(o),a)) db.commit(); db.close()
if __name__ == "__main__":
init_db() print("DB Ready") 
