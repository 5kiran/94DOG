from flask import Flask, jsonify, render_template, request, session, redirect, url_for
import pymysql
import json

app = Flask(__name__)

app.secret_key = 'sad111123'
# db가 아닌 다른 변수명으로 써도 됩니다.
db = pymysql.connect(
  host='127.0.0.1',
  user='root',
  db='dog94',
  password='Jungmin0413',
  charset='utf8')

curs = db.cursor(pymysql.cursors.DictCursor)


# @app.route("/")
# def index():
#   return render_template("index.html")


@app.route("/register", methods = ['GET', 'POST'])
def register_page():
  return render_template("register.html")


@app.route("/login", methods = ['GET', 'POST'])
def login_page():
  return render_template("login.html")

@app.route("/home")
def home_page():
  return render_template("home.html", name = session['name'])

@app.route("/register/in", methods=["POST"])
def register():

  name_receive = request.form.get("name_give")
  email_receive = request.form.get("email_give")
  password_receive = request.form.get("password_give")

  doc = {
    'name': name_receive,
    'email': email_receive,
    'password': password_receive
  }

  curs.execute(f"insert into user (name,email,password) value ('{name_receive}','{email_receive}', '{password_receive}')")
  db.commit()
  db.close()

  return jsonify({'msg': '회원가입 완료'})

@app.route('/login/in', methods = ['POST'])
def login():
  email_receive = request.form['email_give']
  password_receive = request.form['password_give']
  print(email_receive,password_receive)
  curs.execute('SELECT * FROM user WHERE email = %s AND password = %s', (email_receive,password_receive))
  record = curs.fetchall()
  
  if record:
    session['loggedin'] = True
    session['name'] = record[0]['name']
    return jsonify({'msg': '로그인 성공'})
  else:
    return jsonify({'msg':'사용자 정보가 일치하지 않습니다.'})


@app.route('/logout')
def logout():
  session.pop('loggedin', None)
  session.pop('name', None)
  return redirect(url_for('login_page'))

if __name__ == '__main__':
  app.run('0.0.0.0', port=5000, debug=True)