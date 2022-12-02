import asyncio
import websockets

async def hello(websocket, path):
    while True:
        name = await websocket.recv()
        print(name)

async def hello():
    uri = "wss://stream.coinmarketcap.com/price/latest"
    async with websockets.connect(uri) as websocket:
        name = await websocket.recv()
        print(name)

asyncio.get_event_loop().run_until_complete(hello())