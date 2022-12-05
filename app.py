from flask import Flask, jsonify, render_template, request
app = Flask(__name__)

import pymysql


@app.route('/')
def home():
  return render_template('index.html')

@app.route('/boards', methods=['GET'])
def pagination():
  db = pymysql.connect(
      host="localhost", 	# 데이터베이스 주소
      user="root", 	# 유저네임
      passwd="qwer1234", 	# 패스워드
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

  # print(f'page: {page}, total_page: {total_page}, start_page: {start_page}, end_page: {end_page}')
  response = {'boards': boards, 'page': page, 'total_page': total_page, 'start_page': start_page, 'end_page': end_page}

  db.commit()
  db.close()

  return render_template('components/boards.html', response=response)


# board 데이터 넣는 용도
# @app.route('/boards/insert', methods=["GET"])
# def insert():
#   db = pymysql.connect(
#       host="localhost", 	# 데이터베이스 주소
#       user="root", 	# 유저네임
#       passwd="qwer1234", 	# 패스워드
#       db="dog94", 	# 사용할 DB
#       charset="utf8"	# 인코딩
#   )
  
#   cursor = db.cursor()

#   for i in range(32, 92):
#     sql = 'INSERT INTO board (title, content, user_id) VALUES (%s, %s, %s)'
#     cursor.execute(sql, ('test title'+str(i), 'test content'+str(i), 1))

#   db.commit()
#   db.close()
  
#   data = {'name': 'test'}
#   return render_template('components/pagination.html', data=data)



if __name__ == '__main__':
  app.run('0.0.0.0', port=5000, debug=True)