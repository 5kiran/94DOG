from flask import Flask, jsonify, render_template, request, session, redirect, url_for
import pymysql
from flask_bcrypt import Bcrypt
from datetime import datetime
import hashlib
import logging
import os
from db import DB

# logging system setting
if not os.path.isdir('logs'):
  os.mkdir('logs')  # logs 폴더 없을 경우 자동생성
logging.getLogger('werkzeug').disabled = True
logging.basicConfig(filename = "logs/server.log", level = logging.DEBUG
                  # , datefmt = '%Y/%m/%d %H:%M:%S %p'  # 년/월/일 시(12시간단위)/분/초 PM/AM
                  , datefmt = '%Y/%m/%d %H:%M:%S'  # 년/월/일 시(24시간단위)/분/초
                  , format = '%(asctime)s:%(levelname)s:%(message)s')

app = Flask(__name__)

app.secret_key = 'sad111123'
app.config['BCRYPT_LEVEL'] = 10
app.config['SECRET_KEY'] = '125451161361342134'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
bcrypt = Bcrypt(app)


@app.route('/')
def home():
  app.logger.info(f'[{request.method}] {request.path}')
  return render_template('main.html', component_name='boards')


@app.route('/boards', methods=['GET'])
def pagination():
  # 한 페이지의 게시글 수
  ONE_PAGE = 5
  # 한 섹션의 페이지 수
  ONE_SECTION = 5
  # 페이지 기본값
  page = 1
  # 현재 페이지
  if request.args:
    page = int(request.args['p'])

  app.logger.info(f'[{request.method}] {request.path} :: page={page}')

  # 전체 게시글 수
  sql = 'SELECT count(*) as all_count FROM board WHERE deleted = false' 
  conn = DB('dict')
  all_count = conn.select_all(sql)[0]['all_count']
  
  total_page = all_count // ONE_PAGE + (1 if all_count % ONE_PAGE != 0 else 0)

  if total_page == 0:
    response = {'boards': {}, 'page': page, 'total_page': total_page}
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

  sql = f'SELECT board.id,title,user.name,viewcount,board.created_at,file_url,updated_at from board left join `user` ON board.user_id = user.id WHERE deleted = false ORDER BY id DESC LIMIT {ONE_PAGE} OFFSET {(page-1)*5}'
  conn = DB('dict')
  boards = conn.select_all(sql)

  response = {'boards': boards, 'page': page, 'total_page': total_page, 'start_page': start_page, 'end_page': end_page}

  return jsonify({'response': response})


@app.route("/register", methods=['GET'])
def register_page():
  return render_template("components/register.html")


@app.route("/login")
def login_page():
  return render_template("components/login.html")


@app.route("/home")
def home_page():
  return render_template("components/home.html")


@app.route("/register/in", methods=["POST"])
def register():

  name_receive = request.form.get("user_name")
  email_receive = request.form.get("register_email")

  password_receive = str(request.form.get("register_password"))
  pw_hash = bcrypt.generate_password_hash(password_receive).decode('utf-8')
  email_hash = hashlib.sha256(email_receive.encode('utf-8')).hexdigest()
  file = request.files["file_data"]

  if not os.path.isdir("static/upload/image"):
    os.makedirs('static/upload/image')  # upload/image 폴더 없을 경우 자동생성

  insert_list = []
  sql = ''
  if file:
    extension = file.filename.split('.')[-1]
    today = datetime.now()
    mtime = today.strftime('%Y-%m-%d-%H-%M-%S')
    filename = f'{email_hash}-{mtime}.{extension}'
    save_to = f'static/upload/image/{filename}'
    file.save(save_to)

    insert_list = [name_receive, email_receive, pw_hash, filename]
    sql = 'insert into user (name, email,password, image_url) value (%s, %s, %s, %s)'
  else:
    insert_list = [name_receive, email_receive, pw_hash]
    sql = 'insert into user (name, email, password) value (%s, %s, %s)'

  conn = DB('dict')
  conn.save_one(sql, insert_list)


  signup = ""
  upload_file = ""

  if file:
    upload_file = "upload"
  else:
    upload_file = "none"
  app.logger.info(f'[{request.method}] {request.path} :: file_upload={upload_file}')

  if pw_hash:
    signup = "success"
  else:
    signup = "fail"
  
  app.logger.info(f'[{request.method}] {request.path} :: register={signup}')

  return jsonify({'msg': '회원가입 되었습니다.'})


@app.route("/email", methods=["POST"])
def email():
  email_receive = request.form.get("email_give")

  sql = 'SELECT * FROM user WHERE email = %s'
  conn = DB('dict')
  check = conn.select_one(sql, email_receive)

  log_check = ""

  if check:
    log_check = "fail"
  else:
    log_check = "success"
  app.logger.info(f'[{request.method}] {request.path} :: email_check={log_check}')

  if check:
    return jsonify({'msg': '중복된 이메일입니다.'})
  else:
    return jsonify({'msg': '사용 가능한 이메일입니다.'})


@app.route('/login/in', methods=['POST'])
def login():

  email_receive = request.form['email_give']
  password_receive = request.form['password_give']

  sql = 'SELECT * FROM user WHERE email = %s'
  conn = DB('dict')
  record = conn.select_all(sql, email_receive)
  if not record:
    return jsonify({'msg':'사용자 정보가 일치하지 않습니다.'})
  password = record[0]['password']
  hw = bcrypt.check_password_hash(password, password_receive)

  login_email = email_receive

  app.logger.info(f'[{request.method}] {request.path} :: login={login_email}')


  if record and hw == True:
    session['loggedin'] = True
    session['name'] = record[0]['name']
    session['email'] = record[0]['email']
    session['id'] = record[0]['id']
    session['image'] = record[0]['image_url']
    return jsonify({'msg': '로그인 성공'})
  else:
    return jsonify({'msg':'사용자 정보가 일치하지 않습니다.'})


@app.route('/logout')
def logout():
  logout_email = session['email']

  app.logger.info(f'[{request.method}] {request.path} :: logout={logout_email}')
  session.clear()
  return redirect('/')


@app.route('/liked')
def liked():
  return render_template('components/liked.html', name = session['name'], email = session['email'], id = session['id'])


@app.route('/liked',methods=['POST'])
def like():
  
  if len(session)== 0:
    re = 1 
    return jsonify({'msg': re})
  
  user_id = session['id']
  board_id = request.form['board_id_give']
  writer_id = request.form['writer_id_give']

  like_find = f'SELECT * FROM board LEFT JOIN liked ON board.id = liked.board_id WHERE board.id = {board_id} AND liked.user_id = {user_id}'
  conn = DB('dict')
  result = conn.select_one(like_find)
   
  if result is None:
    app.logger.info(f'[{request.method}] {request.path} :: like_user_id={user_id} board_id={board_id} writer_id={writer_id}')

    like_up = f'INSERT INTO liked (user_id,board_id,writer_id) VALUES ({user_id},{board_id},{writer_id})'
    conn = DB('dict')
    conn.save_one(like_up)

    board_like_up = f'UPDATE board SET liked = liked +1 WHERE board.id = {board_id}'
    conn = DB('dict')
    conn.save_one(board_like_up)
    
    liked = f'SELECT liked FROM board where id = {board_id}'
    conn = DB('dict')
    cnt = conn.select_one(liked)
    
    curr = 1
    return jsonify({'cnt': cnt},curr)

  else:
    app.logger.info(f'[{request.method}] {request.path} :: unlike_user_id={user_id} board_id={board_id} writer_id={writer_id}')

    like_delete = f'DELETE FROM liked WHERE liked.user_id = {user_id} AND liked.board_id = {board_id}'
    conn = DB('dict')
    conn.save_one(like_delete)

    board_like_down = f'UPDATE board SET liked = liked -1 WHERE board.id = {board_id}'
    conn = DB('dict')
    conn.save_one(board_like_down)
    
    liked = f'SELECT liked FROM board where id = {board_id}'
    conn = DB('dict')
    cnt = conn.select_one(liked)
    
    curr = 0
    return jsonify({'cnt': cnt},curr)

@app.route("/liked/rank", methods=["GET"])
def like_rank():
  sql = 'SELECT `user`.name,count(writer_id) AS like_cnt FROM liked LEFT JOIN `user`ON liked.writer_id = `user`.id GROUP BY `user`.name ORDER BY  like_cnt DESC LIMIT 5'
  conn = DB('dict')
  like_data = conn.select_all(sql)
  
  return jsonify({'likeRankList' :like_data})


# 수정2
@app.route("/temp")
def post():
    return render_template('main.html', component_name='post')


@app.route("/viewpost-layout")
def viewpost():
    return render_template('main.html', component_name='viewpost')


@app.route("/temp_update")
def post_update():
    return render_template('main.html', component_name='post_update')


# 게시글 저장 기능
@app.route('/post', methods=['POST'])
def save_post():
    if len(session) == 0 :
      return jsonify({'msg': '로그인 후 이용해주세요.'})

    title_receive = request.form.get("title")
    content_receive = request.form.get("content")
    user_id = session['id']
    email_hash = hashlib.sha256(session['email'].encode('utf-8')).hexdigest()
    file = request.files["post_file"]

    sql = ''
    insert_list = []
    if file:
      extension = file.filename.split('.')[-1]
      today = datetime.now()
      mtime = today.strftime('%Y-%m-%d-%H-%M-%S')
      filename = f'{email_hash}-{mtime}.{extension}'
      save_to = f'static/upload/image/{filename}'
      file.save(save_to)

      sql = 'insert into board (title, content, user_id, file_url) value (%s, %s, %s, %s)'
      insert_list = [title_receive, content_receive, user_id, filename]
    else:
      sql = 'insert into board (title, content, user_id) value (%s, %s, %s)'
      insert_list = [title_receive, content_receive, user_id]


    conn = DB('dict')
    conn.save_one(sql, insert_list)
   
    return jsonify({'msg': '게시글 저장 완료!'})

# 게시글 삭제 기능
@app.route('/post/delete', methods=['POST'])
def delete_post():
    if len(session) == 0:
      return jsonify({'msg': '로그인 후 이용해주세요.'})
    
    user_id = session['id']
    id_receive = request.form.get('id_give')
    
    find_user = f'select * from board where user_id = {user_id} and id = {id_receive}'
    conn = DB('dict')
    a = conn.select_one(find_user)

    if a is None:
      return jsonify({'msg': '작성자가 아닙니다.'})
    
    sql = f"update board set deleted=1 where id='{id_receive}'"
    conn = DB('dict')
    conn.save_one(sql)

    return jsonify({'msg': '게시글 삭제 완료!'})


@app.route('/views/<id>', methods=['get'])
def view_post(id):
    sql = f"select board.id, title, liked, content, user.name, user_id, board.created_at, file_url, updated_at, viewcount from board left join `user` ON board.user_id = user.id WHERE board.id='{id}'"
    conn = DB('dict')
    view_post = conn.select_all(sql)

    db = pymysql.connect(
    host='127.0.0.1',
    user='root',
    db='dog94',
    password='dog94',
    charset='utf8')


    curs = db.cursor(pymysql.cursors.DictCursor)

    curs.execute(f"update board set viewcount = board.viewcount + 1 WHERE board.id='{id}'")

    db.commit()
    db.close()


    like_status = 0

    if like_find_user(id) is not None:
      like_status += 1  

    return jsonify({'view_post_list':view_post} , like_status)
  

def like_find_user(board_id):
    if len(session) == 0 :
      return 0

    user_id = session['id']
    
    like_find = f'SELECT * FROM board LEFT JOIN liked ON board.id = liked.board_id WHERE board.id = {board_id} AND liked.user_id = {user_id}'
    conn = DB('dict')
    like_data = conn.select_one(like_find)

    return like_data

  

@app.route('/post/modi', methods=['POST'])
def modi_post():
    if len(session) == 0 :
      return jsonify({'msg': '로그인 후 이용해주세요.'})

    title_receive = request.form.get('title_give')
    content_receive = request.form.get('content_give')
    update_at_receive = request.form.get('data_give')
    id_receive = request.form.get('id_give')
    user_id = session['id']

    find_user = f'select * from board where user_id = {user_id} and id = {id_receive}'
    conn = DB('dict')
    a = conn.select_one(find_user)
    
    if a is None:
      return jsonify({'msg': '작성자가 아닙니다.'})

    sql = 'update board set title=%s, content=%s, updated_at=%s where id=%s'
    update_list = [title_receive, content_receive, update_at_receive, id_receive]
    conn = DB('dict')
    conn.save_one(sql, update_list)

    return jsonify({'msg': '게시글 수정 완료!'})


@app.route('/preview/<id>', methods=['get'])
def preview(id):

    db = pymysql.connect(
    host='127.0.0.1',
    user='root',
    db='dog94',
    password='dog94',
    charset='utf8')

    curs = db.cursor(pymysql.cursors.DictCursor)

    curs.execute(
        f"select * from board WHERE id='{id}'")

    previews = curs.fetchall()


    db.commit()
    return jsonify({'preview_list':previews}) 


PORT = 5000
if __name__ == '__main__':
  app.logger.info('     _______. _______ .______      ____    ____  _______ .______              ______   .__   __. ')
  app.logger.info('    /       ||   ____||   _  \     \   \  /   / |   ____||   _  \            /  __  \  |  \ |  | ')
  app.logger.info('   |   (----`|  |__   |  |_)  |     \   \/   /  |  |__   |  |_)  |          |  |  |  | |   \|  | ')
  app.logger.info('    \   \    |   __|  |      /       \      /   |   __|  |      /           |  |  |  | |  . `  | ')
  app.logger.info('.----)   |   |  |____ |  |\  \----.   \    /    |  |____ |  |\  \----.      |  `--`  | |  |\   | ')
  app.logger.info('|_______/    |_______|| _| `._____|    \__/     |_______|| _| `._____|       \______/  |__| \__| ')
  app.logger.info('                                                                                       PORT='+str(PORT))

  app.run('0.0.0.0', port=PORT, debug=True, use_reloader=False)