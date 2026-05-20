import time, json, pika

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()
channel.queue_declare(queue="adsb_queue")

lat = 7.8804
lon = 98.3923

i = 0
while True:
    lon += 0.001

    data = {
        "now": int(time.time()),
        "messages": i,
        "aircraft": [{
            "hex": "880123",
            "flight": "THA123",
            "lat": lat,
            "lon": lon,
            "altitude": 32000,
            "speed": 450,
            "track": 90,
            "squawk": "7000",
            "rssi": -18.0,
            "seen": 0.5,
            "seen_pos": 0.5,
            "messages": i
        }]
    }

    channel.basic_publish(
        exchange='',
        routing_key='adsb_queue',
        body=json.dumps(data)
    )

    print("sent frame", i)
    i += 1
    time.sleep(1)