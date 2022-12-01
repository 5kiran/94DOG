from flask import Flask, jsonify, render_template, request
app = Flask(__name__)


@app.route('/')
def home():
  return render_template('index.html')


if __name__ == '__main__':
  app.run('0.0.0.0', port=5000, debug=True)