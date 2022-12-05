from flask import Flask, jsonify, render_template, request
import pymysql
app = Flask(__name__)

# db가 아닌 다른 변수명으로 써도 됩니다.
db = pymysql.connect(
    host='127.0.0.1',
    user='root',
    db='dog94',
    password='a123456',
    charset='utf8')

curs = db.cursor(pymysql.cursors.DictCursor)

qurey = db.cursor()


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/temp")
def profile():
    return render_template("post.html")


@app.route("/viewpost-layout")
def viewpost():
    return render_template("viewpost.html")


# 게시글 저장 기능
@app.route('/post', methods=['POST'])
def save_post():

    title_receive = request.form.get('title_give')
    content_receive = request.form.get('content_give')
    date_receive =request.form.get('data_give')
    # created_at_receive = request.form.get('created_at_give')
    
    # 이건 옛날 방식
    # title_receive = request.form['title_give']
    # content_receive = request.form['content_give']

    doc = {
        'title': title_receive,
        'content': content_receive,
        'updated_at': date_receive,
        # 'created_at': created_at_receive
    }

    curs.execute(
        f"insert into board (title,content,updated_at) value ('{title_receive}','{content_receive}','{date_receive}')")
    db.commit()
    # 스트링 합 연산자

    return jsonify({'msg': '게시글 저장 완료!'})


# 게시글 수정 기능
@app.route('/post/update', methods=['POST'])
def update_post():

    title_receive = request.form.get('title_give')
    content_receive = request.form.get('content_give')
    id_receive = request.form.get('id_give')

    doc = {
        'title': title_receive,
        'content': content_receive,
        'id': id_receive,
    }

    curs.execute(
        f"update board set title='{title_receive}',content='{content_receive}' where id='{id_receive}'")
    db.commit()
    # 스트링 합 연산자

    return jsonify({'msg': '게시글 수정 완료!'})


# 게시글 삭제 기능
@app.route('/post/delete', methods=['POST'])
def delete_post():

    id_receive = request.form.get('id_give')

    doc = {
        'id': id_receive,
    }

    curs.execute(
        f"update board set deleted=1 where id='{id_receive}'")
    db.commit()
    # 스트링 합 연산자

    return jsonify({'msg': '게시글 삭제 완료!'})


# 게시글 보기 기능
@app.route('/post', methods=['get'])
def show_post():

    # sql = "select title,content from board"
    sql = "select * from board" 

    qurey.execute(sql)

    people = qurey.fetchall()

    return jsonify({'show_post':people})


# 게시글 타이틀(링크)를 클릭하면 해당 페이지로 이동하는 기능
# 예를 들어 4번 게시글을 클릭하면 4번 게시글의 정보를 받아와서 페이지로 이동
@app.route('/views/<id>', methods=['get'])
def view_post(id):

    curs.execute(
        f"select * from board where id='{id}'")

    view_post = curs.fetchall()

    db.commit()
    return jsonify({'view_post_list':view_post})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5500, debug=True)
