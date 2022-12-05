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


@app.route("/register", methods=['GET'])
def register_page():
  return render_template("components/register.html")


@app.route("/login", methods=['GET', 'POST'])
def login_page():
  return render_template("components/login.html")

@app.route("/home")
def home_page():
  return render_template("components/home.html", name = session['name'], email = session['email'], id = session['id'])

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

@app.route("/email", methods=["POST"])
def email():
  email_receive = request.form.get("email_give")
  print('email_receive =', email_receive)
  curs.execute('SELECT * FROM user WHERE email = %s', (email_receive))
  check = curs.fetchall()
  db.commit()
  print('check:', check)
  if check:
    return jsonify({'msg': '중복된 이메일입니다.'})
  else:
    return jsonify({'msg': '사용 가능한 이메일입니다.'})


@app.route('/login/in', methods=['POST'])
def login():
  email_receive = request.form['email_give']
  password_receive = request.form['password_give']
  curs.execute('SELECT * FROM user WHERE email = %s AND password = %s', (email_receive,password_receive))
  record = curs.fetchall()
  db.commit()
  db.close()
  if record:
    session['loggedin'] = True
    session['name'] = record[0]['name']
    session['email'] = record[0]['email']
    session['id'] = record[0]['id']
    return jsonify({'msg': '로그인 성공'})
  else:
    return jsonify({'msg':'사용자 정보가 일치하지 않습니다.'})

@app.route('/logout')
def logout():
  session.pop('loggedin', None)
  session.pop('name', None)
  return redirect(url_for('login_page'))

@app.route('/liked')
def liked():
  return render_template('components/liked.html')



@app.route('/liked',methods=['POST'])
def like():
  user_id = request.form['user_id_give']
  board_id = request.form['board_id_give']
  writer_id = request.form['writer_id_give']
  like_find = f'SELECT * FROM board LEFT JOIN liked ON board.id = liked.board_id WHERE board.id = {board_id} AND liked.user_id = {user_id}'
  curs.execute(like_find)
  result = curs.fetchone()
  
  
  if result is None:
    like_up = f'INSERT INTO liked (user_id,board_id,writer_id) VALUES ({user_id},{board_id},{writer_id})'
    board_like_up = f'UPDATE board SET liked = liked +1 WHERE board.id = {board_id}'
    curs.execute(like_up)
    curs.execute(board_like_up)
    db.commit()
    
  else:
    like_delete = f'DELETE FROM  liked WHERE liked.user_id = {user_id} AND liked.board_id = {board_id}'
    board_like_down = f'UPDATE board SET liked = liked -1 WHERE board.id = {board_id}'
    curs.execute(like_delete)
    curs.execute(board_like_down)
    db.commit()
    
  return jsonify({'msg': '좋아용'})

@app.route("/liked/board", methods=["GET"])
def board_like():
  board_id = "SELECT id,title,content,file_url,user_id,liked  FROM board WHERE id = 1"
  curs.execute(board_id)
  board_data = curs.fetchone()  
  
  return jsonify({'boardData': board_data})

@app.route("/liked/rank", methods=["GET"])
def like_rank():
  sql = 'SELECT `user`.name,count(writer_id) AS like_cnt FROM liked LEFT JOIN `user`ON liked.writer_id = `user`.id GROUP BY `user`.name ORDER BY  like_cnt DESC LIMIT 5'
  curs.execute(sql)
  like_data = curs.fetchall()
  
  return jsonify({'likeRankList' :like_data})


if __name__ == '__main__':
  app.run('0.0.0.0', port=5000, debug=True)
