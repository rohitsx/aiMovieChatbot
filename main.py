from flask import Flask, request

from src.L1 import L1BasicAPIChatbot
from src.L2 import L2StoreRetrieveMovieScript

app = Flask(__name__)

@app.route('/L1/chat', methods=['POST'])
@app.route('/l1/chat', methods=['POST'])
def L1():
    return L1BasicAPIChatbot.handler(request)


@app.route('/L2/chat', methods=['POST'])
@app.route('/l2/chat', methods=['POST'])
async def L2():
    return await L2StoreRetrieveMovieScript.handler(request)

if __name__ == '__main__':
    app.run(debug=True)
