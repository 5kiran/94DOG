from flask import Flask, jsonify, render_template, request, session
import pymysql
app = Flask(__name__)

# db가 아닌 다른 변수명으로 써도 됩니다.
db = pymysql.connect(
  host='127.0.0.1',
  user='root',
  db='dog94',
  password='Jungmin0413',
  charset='utf8')

curs = db.cursor(pymysql.cursors.DictCursor)


@app.route("/login")
def index():
  return render_template("index.html")

# @app.route('/pythonlogin/', methods=['GET', 'POST'])
# def login():
#     # Output message if something goes wrong...
#     msg = ''
#     return render_template('index.html', msg='')

@app.route("/register")
def register_page():
  return render_template("register.html")


@app.route('/register/in', methods=['POST'])
def register():

  name_receive = request.form.get('name_give')
  email_receive = request.form.get('email_give')
  password_receive = request.form.get('password_give')

  doc = {
    'name': name_receive,
    'email': email_receive,
    'password': password_receive
  }

  curs.execute(f"insert into user (name,email,password) value ('{name_receive}','{email_receive}', '{password_receive}')")
  db.commit()
  # 스트링 합 연산자

  return jsonify({'msg': '회원가입 완료!'})

if __name__ == '__main__':
  app.run('0.0.0.0', port=5000, debug=True)