from fastapi import WebSocket, WebSocketDisconnect
from ..L5.db_operations import get_chat_history
from ..L5.msg_handler import msg_handler


class L5:
    async def handler(self, ws:WebSocket):
        try:

            username = ws.query_params.get("username")
            if not username:
                return

            await ws.accept()
            await ws.send_json({"message":"Connection established"})

            chat_history = await get_chat_history(username)
            await ws.send_json({"chat_history": chat_history})

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

            human_msg = data.get("script")

            if human_msg:
                handler = msg_handler()
                await handler.main(ws, human_msg)
            else:
                raise ValueError("Invalid message or userid")

        except Exception as err:
            print("WebSocket error:",err)
            raise

