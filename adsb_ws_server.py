import json
import websockets
import asyncio # async ใช้ทำให้โปรแกรมทำงานได้หลายส่วนพร้อมกัน
import aiohttp

URL = "https://opensky-network.org/api/states/all"
#URL = "data/aircraft.json"
#URL = "http://localhost:8080/data/aircraft.json"

#fetch data จาก url
async def fetch_adsb(session):
    async with session.get(URL) as response:
        return await response.json()
    
#อ่านไฟล์ json
# async def handler(websocket):
#     async with aiohttp.ClientSession() as session:

#         while True:
#             try:
#                 data = await fetch_adsb(session)

#                 await websocket.send(json.dumps(data))

#             except Exception as e:
#                 print("ADS-B fetch error:", e)

#             await asyncio.sleep(10)

def load_data():
    with open('data/aircraft.json', 'r', encoding='utf-8') as f:
        return json.load(f)

async def handler(websocket):

    while True:

        data = load_data()

        await websocket.send(
            json.dumps(data)
        )

        await asyncio.sleep(1)

async def main():

    server = await websockets.serve(
        handler,
        "0.0.0.0",
        8765
    )

    print("WebSocket ADS-B Server started")

    await server.wait_closed()

asyncio.run(main())



# latest_data = {}
# clients = set()

# async def fetch_loop():

#     global latest_data

#     timeout = aiohttp.ClientTimeout(total=10)

#     async with aiohttp.ClientSession(timeout=timeout) as session:

#         while True:

#             try:

#                 async with session.get(URL) as resp:

#                     if resp.status == 429:
#                         print("Rate limited")
#                         await asyncio.sleep(60)
#                         continue

#                     if resp.status != 200:
#                         print("HTTP error:", resp.status)
#                         await asyncio.sleep(10)
#                         continue

#                     latest_data = await resp.json()

#                     print("ADS-B updated")

#             except Exception as e:
#                 print("Fetch error:", e)

#             # Poll slowly
#             await asyncio.sleep(15)

# async def handler(websocket):

#     clients.add(websocket)

#     print("Client connected")

#     try:

#         while True:

#             if latest_data:
#                 await websocket.send(
#                     json.dumps(latest_data)
#                 )

#             await asyncio.sleep(1)

#     except websockets.ConnectionClosed:
#         pass

#     finally:
#         clients.remove(websocket)
#         print("Client disconnected")

# async def main():

#     # Start background fetcher
#     asyncio.create_task(fetch_loop())

#     server = await websockets.serve(
#         handler,
#         "0.0.0.0",
#         8765
#     )

#     print("WebSocket ADS-B Server started")

#     await server.wait_closed()

# asyncio.run(main())