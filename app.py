from flask import Flask, jsonify, render_template, request, session, redirect, url_for
import pymysql
import bcrypt

app = Flask(__name__)

app.secret_key = 'sad111123'


@app.route('/')
def home():
  return render_template('main.html', component_name='boards')


@app.route('/boards', methods=['GET'])
def pagination():
  db = pymysql.connect(
      host="localhost", 	# 데이터베이스 주소
      user="root", 	# 유저네임
      passwd="dog94", 	# 패스워드
      db="dog94", 	# 사용할 DB
      charset="utf8"	# 인코딩
  )

  # 한 페이지의 게시글 수
  ONE_PAGE = 5
  # 한 섹션의 페이지 수
  ONE_SECTION = 5
  # 페이지 기본값
  page = 1
  # 현재 페이지
  if request.args:
    page = int(request.args['p'])

  # 전체 게시글 수
  cursor = db.cursor(pymysql.cursors.DictCursor)
  sql = 'SELECT count(*) as all_count FROM board WHERE deleted = false' 
  cursor.execute(sql)
  all_count = cursor.fetchall()[0]['all_count']

  total_page = all_count // ONE_PAGE + (1 if all_count % ONE_PAGE != 0 else 0)

  if total_page == 0:
    response = {'boards': {}, 'page': page, 'total_page': total_page}
    db.commit()
    db.close()
    return jsonify({'response': response})

  if page < 1 or page > total_page:
    print('잘못된 페이지 요청 예외처리')
    return render_template('components/fail.html')

  start_page = (page - 1) // ONE_SECTION * ONE_SECTION
  if start_page % ONE_SECTION == 0:
    start_page += 1
  
  end_page = start_page + ONE_SECTION - 1
  if end_page > total_page:
    end_page = total_page

  sql = f'SELECT * FROM board WHERE deleted = false ORDER BY id DESC LIMIT {ONE_PAGE} OFFSET {(page-1)*5}'
  cursor.execute(sql)
  boards = cursor.fetchall()

  response = {'boards': boards, 'page': page, 'total_page': total_page, 'start_page': start_page, 'end_page': end_page}

  db.commit()
  db.close()

  return jsonify({'response': response})


# board 데이터 넣는 용도. 주석 없애고 실행
@app.route('/boards/insert', methods=["GET"])
def insert():
  db = pymysql.connect(
      host="localhost", 	# 데이터베이스 주소
      user="root", 	# 유저네임
      passwd="dog94", 	# 패스워드
      db="dog94", 	# 사용할 DB
      charset="utf8"	# 인코딩
  )
  
  cursor = db.cursor()

  for i in range(1, 20):
    sql = 'INSERT INTO board (title, content, user_id) VALUES (%s, %s, %s)'
    cursor.execute(sql, ('test title'+str(i), 'test content'+str(i), 3))

  db.commit()
  db.close()
  
  data = {'name': 'test'}
  return render_template('components/pagination.html', data=data)







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
  db = pymysql.connect(
  host='127.0.0.1',
  user='root',
  db='dog94',
  password='dog94',
  charset='utf8')
  curs = db.cursor(pymysql.cursors.DictCursor)

  name_receive = request.form.get("name_give")
  email_receive = request.form.get("email_give")
  pw_hash = bcrypt.generate_password_hash(password_receive).decode('utf-8')

  curs.execute(f"insert into user (name,email,password) value ('{name_receive}','{email_receive}', '{pw_hash}')")
  db.commit()
  db.close()

  return jsonify({'msg': '회원가입 완료'})


@app.route("/email", methods=["POST"])
def email():
  db = pymysql.connect(
  host='127.0.0.1',
  user='root',
  db='dog94',
  password='dog94',
  charset='utf8')
  curs = db.cursor(pymysql.cursors.DictCursor)

  email_receive = request.form.get("email_give")

  curs.execute('SELECT * FROM user WHERE email = %s', (email_receive))
  check = curs.fetchall()
  db.commit()
  db.close()

  if check:
    return jsonify({'msg': '중복된 이메일입니다.'})
  else:
    return jsonify({'msg': '사용 가능한 이메일입니다.'})


@app.route('/login/in', methods=['POST'])
def login():
  db = pymysql.connect(
  host='127.0.0.1',
  user='root',
  db='dog94',
  password='dog94',
  charset='utf8')
  curs = db.cursor(pymysql.cursors.DictCursor)

  email_receive = request.form['email_give']
  password_receive = request.form['password_give']
  pw_hash = bcrypt.generate_password_hash(password_receive).decode('utf-8')
  hw = bcrypt.check_password_hash(pw_hash, password_receive)
  curs.execute('SELECT * FROM user WHERE email = %s', (email_receive))
  record = curs.fetchall()
  db.commit()
  db.close()

  if record and hw == True:
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
  return render_template('components/liked.html', name = session['name'], email = session['email'], id = session['id'])


@app.route('/liked',methods=['POST'])
def like():
  db = pymysql.connect(
  host='127.0.0.1',
  user='root',
  db='dog94',
  password='dog94',
  charset='utf8')
  curs = db.cursor(pymysql.cursors.DictCursor)

  user_id = session['id']
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
  else:
    like_delete = f'DELETE FROM  liked WHERE liked.user_id = {user_id} AND liked.board_id = {board_id}'
    board_like_down = f'UPDATE board SET liked = liked -1 WHERE board.id = {board_id}'
    curs.execute(like_delete)
    curs.execute(board_like_down)
    
  db.commit()
  db.close()
    
  return jsonify({'msg': '좋아용'})


@app.route("/liked/board", methods=["GET"])
def board_like():
  db = pymysql.connect(
  host='127.0.0.1',
  user='root',
  db='dog94',
  password='dog94',
  charset='utf8')
  curs = db.cursor(pymysql.cursors.DictCursor)
  
  temp_num = 5
  board_id = f'SELECT id,title,content,file_url,user_id,liked  FROM board WHERE id = {temp_num}'
  curs.execute(board_id)
  board_data = curs.fetchone()
  
  like_status = 0
  if like_find_user(temp_num,curs) is not None:
    like_status += 1  

  db.commit()
  db.close()
  
  return jsonify({'boardData': board_data},like_status)

def like_find_user(board_id,curs):
  user_id = session['id']
  
  like_find = f'SELECT * FROM board LEFT JOIN liked ON board.id = liked.board_id WHERE board.id = {board_id} AND liked.user_id = {user_id}'
  curs.execute(like_find)
  like_data = curs.fetchone()
  
  return like_data


@app.route("/liked/rank", methods=["GET"])
def like_rank():
  db = pymysql.connect(
  host='127.0.0.1',
  user='root',
  db='dog94',
  password='dog94',
  charset='utf8')
  curs = db.cursor(pymysql.cursors.DictCursor)

  sql = 'SELECT `user`.name,count(writer_id) AS like_cnt FROM liked LEFT JOIN `user`ON liked.writer_id = `user`.id GROUP BY `user`.name ORDER BY  like_cnt DESC LIMIT 5'
  curs.execute(sql)
  like_data = curs.fetchall()
  db.commit()
  db.close()
  
  return jsonify({'likeRankList' :like_data})




@app.route("/temp")
def profile():
    return render_template("components/post.html")


@app.route("/viewpost-layout")
def viewpost():
    return render_template("components/viewpost.html")


# 게시글 저장 기능
@app.route('/post', methods=['POST'])
def save_post():

    db = pymysql.connect(
    host='127.0.0.1',
    user='root',
    db='dog94',
    password='dog94',
    charset='utf8')

    curs = db.cursor(pymysql.cursors.DictCursor)

    title_receive = request.form.get('title_give')
    content_receive = request.form.get('content_give')
    date_receive =request.form.get('data_give')

    curs.execute(
        f"insert into board (title,content,updated_at) value ('{title_receive}','{content_receive}','{date_receive}')")
    db.commit()


    return jsonify({'msg': '게시글 저장 완료!'})


# 게시글 수정 기능
@app.route('/post/update', methods=['POST'])
def update_post():

    db = pymysql.connect(
    host='127.0.0.1',
    user='root',
    db='dog94',
    password='dog94',
    charset='utf8')

    curs = db.cursor(pymysql.cursors.DictCursor)

    title_receive = request.form.get('title_give')
    content_receive = request.form.get('content_give')
    id_receive = request.form.get('id_give')


    curs.execute(
        f"update board set title='{title_receive}',content='{content_receive}' where id='{id_receive}'")
    db.commit()

    return jsonify({'msg': '게시글 수정 완료!'})


# 게시글 삭제 기능
@app.route('/post/delete', methods=['POST'])
def delete_post():

    db = pymysql.connect(
    host='127.0.0.1',
    user='root',
    db='dog94',
    password='dog94',
    charset='utf8')

    curs = db.cursor(pymysql.cursors.DictCursor)

    id_receive = request.form.get('id_give')

    curs.execute(
        f"update board set deleted=1 where id='{id_receive}'")
    db.commit()

    return jsonify({'msg': '게시글 삭제 완료!'})


# 게시글 보기 기능
@app.route('/post', methods=['get'])
def show_post():

    db = pymysql.connect(
    host='127.0.0.1',
    user='root',
    db='dog94',
    password='dog94',
    charset='utf8')

    query = db.cursor()

    sql = "select * from board" 

    query.execute(sql)

    people = query.fetchall()

    return jsonify({'show_post':people})


# 게시글 타이틀(링크)를 클릭하면 해당 페이지로 이동하는 기능
# 예를 들어 4번 게시글을 클릭하면 4번 게시글의 정보를 받아와서 페이지로 이동
@app.route('/views/<id>', methods=['get'])
def view_post(id):

    db = pymysql.connect(
    host='127.0.0.1',
    user='root',
    db='dog94',
    password='dog94',
    charset='utf8')

    curs = db.cursor(pymysql.cursors.DictCursor)

    curs.execute(
        f"select * from board where id='{id}'")

    view_post = curs.fetchall()

    db.commit()
    return jsonify({'view_post_list':view_post})



if __name__ == '__main__':
  app.run('0.0.0.0', port=5000, debug=True)
