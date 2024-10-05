from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return jsonify({ "message": "Hello, Client!" })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)