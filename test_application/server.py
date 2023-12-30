from robyn import Robyn, jsonify, WebSocket

app = Robyn(__file__)
websocket = WebSocket(app, "/web_socket")

@websocket.on("message")
def connect(ws, msg):
    print(msg)
    print(ws)
    return message

@websocket.on("close")
def close():
    return '{"message": "Goodbye"}'

@websocket.on("connect")
def message():
    return '{"message": "Hello world, from ws"}'

if __name__ == "__main__":
    app.start()
