import os
import json
import websocket
from dotenv import load_dotenv
import base64
import json
import struct
import soundfile as sf
from websocket import create_connection

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



def float_to_16bit_pcm(float32_array):
    clipped = [max(-1.0, min(1.0, x)) for x in float32_array]
    pcm16 = b''.join(struct.pack('<h', int(x * 32767)) for x in clipped)
    return pcm16

def base64_encode_audio(float32_array):
    pcm_bytes = float_to_16bit_pcm(float32_array)
    encoded = base64.b64encode(pcm_bytes).decode('ascii')
    return encoded

filename = "output.wav"  # Path to your WAV file
data, samplerate = sf.read(filename, dtype='float32')  
channel_data = data[:, 0] if data.ndim > 1 else data
fullAudio = base64_encode_audio(channel_data)

# fullAudio = "<a base64-encoded string of audio bytes>"

event = {
    "type": "conversation.item.create",
    "item": {
        "type": "message",
        "role": "user",
        "content": [
            {
                "type": "input_audio",
                "audio": fullAudio,
            }
        ],
    },
}



# print("Event:", event)
def on_open(ws):
    print("✅ Connected to server.")
    
    # Send event **only after connection is open**
    ws.send(json.dumps(event))
    print("📝 Sent session update.")



# def on_message(ws, message):
#     server_event = json.loads(message)
#     print("Server event:", server_event.get("type"))
#     # (server_event.type)
#     if server_event.get("type") == "response.done":
#         print(server_event["response"]["output"][0])



def on_message(ws, message):
    server_event = json.loads(message)
    print("Server event:", server_event)
    if server_event.get("type") == "response.audio.delta":
        # Access Base64-encoded audio chunks:
        print(server_event.delta)

# Initialize WebSocket connection
ws = websocket.WebSocketApp(
    url,
    header=headers,
    on_open=on_open,  # Send event after connection
    on_message=on_message,
)

ws.run_forever()