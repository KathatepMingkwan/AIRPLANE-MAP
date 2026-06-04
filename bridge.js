const { ConnectionFactory } = require("activemq-client");
const WebSocket = require("ws");

// WebSocket server for your UI
const wss = new WebSocket.Server({ port: 8765 });

wss.on("connection", () => {
    console.log("Frontend connected");
});

function broadcast(data) {
    const msg = JSON.stringify(data);
    wss.clients.forEach(client => {
        if (client.readyState === 1) {
            client.send(msg);
        }
    });
}

// ActiveMQ OpenWire connection
const factory = new ConnectionFactory(
    "tcp://10.76.100.83:61616"
);

factory.createConnection((err, connection) => {
    if (err) {
        console.error("Connection error:", err);
        return;
    }

    connection.start((err) => {
        if (err) {
            console.error("Start error:", err);
            return;
        }

        connection.createSession(false, 1, (err, session) => {
            if (err) return console.error(err);

            const destination = session.createTopic("/topic/aircraft");

            session.createConsumer(destination, (err, consumer) => {
                if (err) return console.error(err);

                console.log("Subscribed to /topic/aircraft");

                consumer.on("message", (message) => {
                    try {
                        const text = message.getText();
                        const data = JSON.parse(text);

                        broadcast(data);
                    } catch (e) {
                        console.error("Parse error:", e);
                    }
                });
            });
        });
    });
});