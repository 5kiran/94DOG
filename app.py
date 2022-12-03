from flask import Flask, jsonify, render_template, request
app = Flask(__name__)


@app.route('/')
def home():
  return render_template('index.html')


@app.route('/pagination', methods=['GET'])
def pagination():
  data = {'name': 'test'}
  return render_template('components/pagination.html', data=data)

if __name__ == '__main__':
  app.run('0.0.0.0', port=5000, debug=True)