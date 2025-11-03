from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, World! This is a test page."

if __name__ == '__main__':
    print("Starting simple Flask app...")
    app.run(debug=True, host='0.0.0.0', port=5001)
