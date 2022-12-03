from flask import Flask, jsonify, render_template, request
app = Flask(__name__)

import pymysql

db = pymysql.connect(host="localhost",
                     port=3306,
                     user="root",
                     db='dog94',
                     password='1qaz12',
                     charset='utf8')

curs = db.cursor()

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/liked')
def liked():
  return render_template('liked.html')

@app.route('/liked',methods=['POST'])
def like():
  user_id = request.form['user_id_give']
  board_id = request.form['board_id_give']
  like_find = f'SELECT * FROM board LEFT JOIN liked ON board.id = liked.board_id WHERE board.id = {board_id} AND liked.user_id = {user_id}'
  curs.execute(like_find)
  result = curs.fetchone()
  print(result)
  if result is None:
    like_up = f'INSERT INTO liked (user_id,board_id) VALUES ({user_id},{board_id})'
    curs.execute(like_up)
    board_like_up = f'UPDATE board SET liked = liked +1 WHERE board.id = {board_id}'
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
  board_id = "SELECT id,title,content,file_url,user_id,liked  FROM board WHERE id = 2"
  curs.execute(board_id)
  board_data = curs.fetchone()
  
  like_num = 'SELECT count(liked.board_id) FROM board LEFT JOIN liked ON board.id = liked.board_id WHERE board.id = 2'
  curs.execute(like_num)
  like_count = curs.fetchone()
  print(like_count)
  
  like_board = [
    like_count,
    board_data
  ]
  
  
  return jsonify({'boardData': like_board})

if __name__ == '__main__':
  app.run('0.0.0.0', port=5000, debug=True)
