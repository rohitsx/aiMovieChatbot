from flask import Flask, request

from src.L1 import L1BasicAPIChatbot

app = Flask(__name__)

@app.route('/L1/chat', methods=['POST'])
@app.route('/l1/chat', methods=['POST'])
def L1():
    return L1BasicAPIChatbot.handler(request)


@app.route('/L2/chat', methods=['POST'])
@app.route('/l2/chat', methods=['POST'])
def L2():
    print(request.json)
    return "heloow\n"

if __name__ == '__main__':
    app.run(debug=True)
