from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "🚀 Hello from Flask App on Kubernetes with Jenkins!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
