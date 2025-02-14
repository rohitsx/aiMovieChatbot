from flask import Flask, request
import asyncio


from src.L1 import L1BasicAPIChatbot
from src.L2 import L2StoreRetrieveMovieScript, scriptScraper
from src.L3 import L3ImplementRAGwithVectorSearch, updateVectorDb

app = Flask(__name__)

@app.route('/chat/L1', methods=['POST'])
@app.route('/chat/l1', methods=['POST'])
def L1():
    return L1BasicAPIChatbot.handler(request)


@app.route('/chat/L2', methods=['POST'])
@app.route('/chat/l2', methods=['POST'])
async def L2():
    return await L2StoreRetrieveMovieScript.handler(request)


@app.route('/chat/L3', methods=['POST'])
@app.route('/chat/l3', methods=['POST'])
async def L3():
    return L3ImplementRAGwithVectorSearch.handler(request)


if __name__ == '__main__':
    asyncio.run(scriptScraper.main())
    asyncio.run(updateVectorDb.main())
    app.run(debug=True)
