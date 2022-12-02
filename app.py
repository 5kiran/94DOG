from flask import Flask, render_template, request, jsonify
import pymysql

app = Flask(__name__)

@app.route('/register')
def register():
    return render_template('register.html')

db = pymysql.connect(host="localhost",
                      port=3306,
                      user="root",
                      db='dog94',
                      password='Jungmin0413',
                      charset='utf8')

curs = db.cursor()

@app.route("/register", methods=["POST"])
def user_register():
  params = request.get_json()
  name = params['name']
  psword = params['psword']
  email = params['email']

  sql = """insert into user (name, email, psword)
            values (%s,%s,%s)
        """
  curs.execute(sql, (name, email, psword))
  curs.fetchall()
  db.commit()
  print(params)
  return "ok"

if __name__ == '__main__':
  app.run('0.0.0.0', port=5000, debug=True)