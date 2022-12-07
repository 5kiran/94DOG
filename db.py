import pymysql

class DB:
  def __init__(self, dict):
    self.con = pymysql.connect(
      host='localhost',
      user='root',
      password='dog94',
      db='dog94',
      charset='utf8',  # 한글처리 (charset = 'utf8')
      autocommit=True,  # 결과 DB 반영 (Insert or update)
    )
    if dict=='dict':
      self.cur = self.con.cursor(pymysql.cursors.DictCursor)
    else:
      self.cur = self.con.cursor()

  def select_one(self, sql, args=None):
    self.cur.execute(sql, args)
    result = self.cur.fetchone()
    self.cur.close()
    self.con.close()
    return result
    
  def select_all(self, sql, args=None):
    self.cur.execute(sql, args)
    result = self.cur.fetchall()
    self.cur.close()
    self.con.close()
    return result

  def save_one(self, sql, args=None):
    result = self.cur.execute(sql, args)
    self.cur.close()
    self.con.close()
    return result

  def save_all(self, sql, args=None):
    result = self.cur.executemany(sql, args)
    self.cur.close()
    self.con.close()
    return result