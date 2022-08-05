from flask import Flask

app = Flask(__name__)
#按播放鍵執行程式
@app.route("/")
def hello():
    return "Hello, World!"
if __name__ == '__main__':
    app.debug = True
    app.run()
