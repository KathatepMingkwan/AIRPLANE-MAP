import json
import websockets
import asyncio
import aiohttp

URL = "http://localhost:8080/data/aircraft.json"

async def fetch_adsb(session):
    async with session.get(URL) as resp:
        return await resp.json()
    
async def handler(websocket):
    async with aiohttp.ClientSession() as session:

        while True:
            try:
                data = await fetch_adsb(session)

                await websocket.send(json.dumps(data))

            except Exception as e:
                print("ADS-B fetch error:", e)

            await asyncio.sleep(1)

# def load_data():
#     with open('data/aircraft.json', 'r', encoding='utf-8') as f:
#         return json.load(f)

# async def handler(websocket):

#     while True:

#         data = load_data()

#         await websocket.send(
#             json.dumps(data)
#         )

#         await asyncio.sleep(1)

async def main():

    server = await websockets.serve(
        handler,
        "0.0.0.0",
        8765
    )

    print("WebSocket ADS-B Server started")

    await server.wait_closed()

asyncio.run(main())