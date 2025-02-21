from fastapi import Depends, FastAPI, Request, WebSocket
from contextlib import asynccontextmanager
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from redis.asyncio import Redis
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
import uvicorn

from src.lib import script_scraper, update_vectorDb
from src.L1 import L1_basic_API_chatbot
from src.L2 import L2_store_retrieve_MovieScript
from src.L3 import L3_implement_RAG_with_vectorSearch
from src.L4 import L4_scale
from src.L5.L5_optimize_for_latency import L5
from src.lib.db.psql import create_table, create_chat_history_table
from src.L5.db_operations import check_username_exits
from src.lib.env import config

@asynccontextmanager
async def lifespan(_: FastAPI):
    if not config["REDIS_URL"]:
        raise ValueError("REDIS_URL is not set in .env")
    redis_connection = Redis.from_url(config["REDIS_URL"], encoding="utf8")
    await FastAPILimiter.init(redis_connection)

    await create_table()
    await create_chat_history_table()

    await script_scraper.main() 
    await update_vectorDb.main()
    print("Background tasks completed.")

    yield
    await FastAPILimiter.close()


app = FastAPI(lifespan=lifespan)
rate_limite = [Depends(RateLimiter(times=5, seconds=1))]

if not config["ORIGINS"]:
    raise ValueError("ORIGINS is not set in .env")

app.add_middleware(
    CORSMiddleware,
    allow_origins=config["ORIGINS"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


templates = Jinja2Templates(directory="templates")
@app.get('/')
def home(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )

@app.post('/chat/L1', dependencies=rate_limite)
@app.post('/chat/l1', dependencies=rate_limite)
async def L1(req: Request):
    return await L1_basic_API_chatbot.handler(req)


@app.post('/chat/L2', dependencies=rate_limite)
@app.post('/chat/l2', dependencies=rate_limite)
async def L2(req: Request):
    return await L2_store_retrieve_MovieScript.handler(req)


@app.post('/chat/L3', dependencies=rate_limite)
@app.post('/chat/l3', dependencies=rate_limite)
async def L3(req: Request):
    return await L3_implement_RAG_with_vectorSearch.handler(req)


@app.post('/chat/L4', dependencies=rate_limite)
@app.post('/chat/l4', dependencies=rate_limite)
async def L4(req: Request):
    return await L4_scale.handler(req)


@app.websocket("/chat/L5")
@app.websocket("/chat/l5")
async def websocket_endpoint(websocket: WebSocket):
    try:
        l5_instance = L5()
        await l5_instance.handler(websocket)
    except Exception:
        pass

@app.post("/chat/check_username_exits/{username}", dependencies=rate_limite)
async def check_username_exits_endpoint(username: str):
    return await check_username_exits(username)


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
