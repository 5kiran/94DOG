from flask import Flask, jsonify, render_template, request
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


@app.route("/temp")
def profile():
  return render_template("register.html")


@app.route('/register', methods=['POST'])
def save_post():

  name_receive = request.form.get('name_give')
  email_receive = request.form.get('email_give')
  psword_receive = request.form.get('psword_give')

  doc = {
    'name': name_receive,
    'email': email_receive,
    'psword': psword_receive
  }

  curs.execute(f"insert into user (name,email,psword) value ('{name_receive}','{email_receive}', '{psword_receive}')")
  db.commit()
  # 스트링 합 연산자

  return jsonify({'msg': '회원가입 완료!'})


if __name__ == '__main__':
  app.run('0.0.0.0', port=5000, debug=True)