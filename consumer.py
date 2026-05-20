import pika
import asyncio
import websockets
import threading

clients = set()

async def ws_handler(websocket):
    clients.add(websocket)
    try:
        async for _ in websocket:
            pass
    finally:
        clients.remove(websocket)

async def broadcast(message):
    if clients:
        await asyncio.gather(*[c.send(message) for c in clients])

def rabbitMQ_consumer(loop):
    #เชื่อมต่อ RabbitMQ server
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost')
    )

    #สร้างช่อง ติดต่อ
    channel = connection.channel()

    #สร้าง queue
    channel.queue_declare(queue='adsb_queue')


    def callback(ch, method, properties, body):
        # print("Received:", body.decode())

        msg = body.decode()
        asyncio.run_coroutine_threadsafe(
            broadcast(msg),
            loop
        )

    channel.basic_consume(
            queue='adsb_queue',
            on_message_callback=callback,
            auto_ack=True
    )

    print("RabbitMQ consumer started")
    channel.start_consuming()

async def main():
    loop = asyncio.get_running_loop()

    #websocket server for browser
    server = await websockets.serve(ws_handler, "localhost", 8765)
    print("WebSocket server running on ws://localhost:8765")

    #rabbitMQ in background thread
    threading.Thread(target=rabbitMQ_consumer, args=(loop,), daemon=True).start()

    await server.wait_closed()

asyncio.run(main())