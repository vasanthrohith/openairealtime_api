import os
import json
import websocket
from dotenv import load_dotenv


# Load environment variables
load_dotenv(override=True)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# print("OPENAI_API_KEY:", OPENAI_API_KEY)

# WebSocket URL and headers
url = "wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview-2024-12-17"
headers = [
    "Authorization: Bearer " + OPENAI_API_KEY,
    "OpenAI-Beta: realtime=v1"
]

# Define event
event = {
    "type": "response.create",
    "response": {
        "modalities": [ "text", "audio" ],
    }
}
# ws.send(json.dumps(event))


def on_open(ws):
    print("✅ Connected to server.")
    
    # Send event **only after connection is open**
    ws.send(json.dumps(event))
    print("📝 Sent session update.")

def on_message(ws, message):
    server_event = json.loads(message)
    print("Server event:", server_event.get("type"))
    # (server_event.type)
    if server_event.get("type") == "response.done":
        print(server_event["response"]["output"][0])

# Initialize WebSocket connection
ws = websocket.WebSocketApp(
    url,
    header=headers,
    on_open=on_open,  # Send event after connection
    on_message=on_message,
)

ws.run_forever()
