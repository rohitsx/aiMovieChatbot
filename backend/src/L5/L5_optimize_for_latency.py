from fastapi import WebSocket, WebSocketDisconnect
from ..L5 import user_handler
from ..L5.msg_handler import msg_handler


class L5:
    async def handler(self, ws:WebSocket):
        try:
            await ws.accept()
            while True:
                try:
                    await self.route_handler(ws)
                except WebSocketDisconnect:
                    break  
                except Exception:
                    pass
        finally:
            await ws.close()

    async def route_handler(self, ws:WebSocket):
        try:
            data = await ws.receive_json()

            userid = data.get("userid")
            create_user_id = data.get("username")
            human_msg = data.get("human_msg")

            if userid:
                await user_handler.get_chat_history(userid)

            elif create_user_id:
               await user_handler.create_userid(create_user_id)

            elif human_msg:
                handler = msg_handler()
                await handler.main(ws, human_msg)

            else:
                raise ValueError("Invalid message or userid")
        except Exception as err:
            print("WebSocket error:",err)
            raise

