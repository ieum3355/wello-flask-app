from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, Wello!'

# 아래 줄은 삭제하거나 주석 처리!
# if __name__ == '__main__':
#     app.run()
