const stompit = require('stompit');
const WebSocket = require('ws');

let messageCount = 0;

// WebSocket server for frontend
const wss = new WebSocket.Server({ port: 8765 });

wss.on('connection', (ws) => {
    console.log('Frontend connected');
});

// Broadcast helper
function broadcast(data) {
    const msg = JSON.stringify(data);

    wss.clients.forEach(client => {
        if (client.readyState === 1) {
            client.send(msg);
        }
    });
}

// ActiveMQ connection
const connectOptions = {
    host: '192.168.137.7',
    port: 61613,
    connectHeaders: {
        host: '/',
        login: 'mams',
        passcode: 'mams'
    }
};

stompit.connect(connectOptions, (error, client) => {
    if (error) {
        console.error('ActiveMQ connection error:', error);
        return;
    }

    console.log('Connected to ActiveMQ');

    const subscribeHeaders = {
        destination: '/topic/GS21_VTSP_MAMS_Topic',
        ack: 'auto'
    };

    client.subscribe(subscribeHeaders, (error, message) => {
        if (error) {
            console.error('Subscribe error:', error);
            return;
        }

        message.readString('utf-8', (error, body) => {
            if (error) return;

            try {
                const data = JSON.parse(body);

                console.log("FROM ACTIVEMQ:", body);

                // normalize to your frontend schema
                const aircraft = {
                    hex: data.AircraftAddress,
                    flight: data.CallSign,
                    lat: data.Lat,
                    lon: data.Lon,
                    altitude: data.Altitude,
                    speed: data.GroundSpeed,
                    track: data.Heading,
                    vert_rate: data.Baro_VR,
                    seen: 0,
                    seen_pos: 0,
                    squawk: null,
                    rssi: 0,
                    position: [data.Lon, data.Lat]
                };

                messageCount++;
                const wrapped = {
                    now: Date.now() / 1000,
                    messages: messageCount,
                    aircraft: [aircraft]   // IMPORTANT: array wrapper   
                };

                // forward to frontend
                broadcast(wrapped);

            } catch (e) {
                console.error('Invalid JSON:', e);
            }
        });
    });
});