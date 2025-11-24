from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def home():
    return jsonify({"message": "Welcome to Flask API"})


@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
