import os
import json
import base64
import asyncio
import websockets
from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from fastapi.websockets import WebSocketDisconnect
# from twilio.twiml.voice_response import VoiceResponse, Connect, Say, Stream
from dotenv import load_dotenv

# load_dotenv()
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


# Configuration
# OPENAI_API_KEY = os.getenv('OPENAI_API_KEY') # requires OpenAI Realtime API Access
# PORT = int(os.getenv('PORT', 5050))
# SYSTEM_MESSAGE = (
#     "You are a helpful and bubbly AI assistant who loves to chat about "
#     "anything the user is interested in and is prepared to offer them facts. "
#     "You can start with: Hi, what can I do for you?"
# )

SYSTEM_MESSAGE = (
    "You are a helpful AI assistant"
    "anything the user is interested in and is prepared to offer them facts. "
    "You can start with: Hi, what can I do for you?"
)


# "You have a penchant for dad jokes, owl jokes, and rickrolling – subtly. "
# Always stay positive, but work in a joke when appropriate.
VOICE = 'alloy'
LOG_EVENT_TYPES = [
    'response.content.done', 'rate_limits.updated', 'response.done',
    'input_audio_buffer.committed', 'input_audio_buffer.speech_stopped',
    'input_audio_buffer.speech_started', 'session.created'
]

app = FastAPI()

if not OPENAI_API_KEY:
    raise ValueError('Missing the OpenAI API key. Please set it in the .env file.')

# @app.get("/", response_class=HTMLResponse)
# async def index_page():
#     return {"message": "Twilio Media Stream Server is running!"}

# @app.api_route("/incoming-call", methods=["GET", "POST"])
# async def handle_incoming_call(request: Request):
#     """Handle incoming call and return TwiML response to connect to Media Stream."""
#     # response = VoiceResponse()
#     # <Say> punctuation to improve text-to-speech flow
#     # response.say("Please wait while we connect your call to the A. I. voice assistant, powered by Twilio and the Open-A.I. Realtime API")
#     response.pause(length=1)
#     response.say("we can chat now！")
#     # response.say("O.K. you can start talking!")
#     host = request.url.hostname
#     print(host)
#     connect = Connect()
#     connect.stream(url=f'wss://{host}/media-stream')
#     response.append(connect)
#     return HTMLResponse(content=str(response), media_type="application/xml")

# @app.websocket("/media-stream")
# async def handle_media_stream(websocket: WebSocket):
#     """Handle WebSocket connections between Twilio and OpenAI."""
#     print("Client connected")
#     await websocket.accept()

#     async with websockets.connect(
#         'wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview-2024-10-01',
#         extra_headers={
#             "Authorization": f"Bearer {OPENAI_API_KEY}",
#             "OpenAI-Beta": "realtime=v1"
#         }
#     ) as openai_ws:
#         await send_session_update(openai_ws)
#         stream_sid = None

#         async def receive_from_twilio():
#             """Receive audio data from Twilio and send it to the OpenAI Realtime API."""
#             nonlocal stream_sid
#             try:
#                 async for message in websocket.iter_text():
#                     data = json.loads(message)
#                     print('----'* 50)
#                     print('data in receive_from_twilio:', data)
#                     print('---'* 50)
#                     if data['event'] == 'media' and openai_ws.open:
#                         audio_append = {
#                             "type": "input_audio_buffer.append",
#                             "audio": data['media']['payload']
#                         }
#                         await openai_ws.send(json.dumps(audio_append))
#                     elif data['event'] == 'start':
#                         stream_sid = data['start']['streamSid']
#                         print(f"Incoming stream has started {stream_sid}")
#             except WebSocketDisconnect:
#                 print("Client disconnected.")
#                 if openai_ws.open:
#                     await openai_ws.close()

#         async def send_to_twilio():
#             """Receive events from the OpenAI Realtime API, send audio back to Twilio."""
#             nonlocal stream_sid
#             try:
#                 async for openai_message in openai_ws:
#                     response = json.loads(openai_message)
#                     if response['type'] in LOG_EVENT_TYPES:
#                         print(f"Received event: {response['type']}", response)
#                     if response['type'] == 'session.updated':
#                         print("Session updated successfully:", response)
#                     if response['type'] == 'input_audio_buffer.speech_started':
#                         await websocket.send_json({ "event": "clear",
#                                                     "streamSid": stream_sid })
#                     if response['type'] == 'response.audio.delta' and response.get('delta'):
#                         # Audio from OpenAI
#                         try:
#                             audio_payload = base64.b64encode(base64.b64decode(response['delta'])).decode('utf-8')
#                             audio_delta = {
#                                 "event": "media",
#                                 "streamSid": stream_sid,
#                                 "media": {
#                                     "payload": audio_payload
#                                 }
#                             }
#                             await websocket.send_json(audio_delta)
#                         except Exception as e:
#                             print(f"Error processing audio data: {e}")
#             except Exception as e:
#                 print(f"Error in send_to_twilio: {e}")

#         await asyncio.gather(receive_from_twilio(), send_to_twilio())

# async def send_session_update(openai_ws):
#     """Send session update to OpenAI WebSocket."""
#     session_update = {
#         "type": "session.update",
#         "session": {
#             "turn_detection": {"type": "server_vad"},
#             "input_audio_format": "g711_ulaw",
#             "output_audio_format": "g711_ulaw",
#             "voice": VOICE,
#             "instructions": SYSTEM_MESSAGE,
#             "modalities": ["text", "audio"],
#             "temperature": 0.8,
#         }
#     }
#     print('Sending session update:', json.dumps(session_update))
#     await openai_ws.send(json.dumps(session_update))

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=PORT)





# connecting to openai/===================


# this are the pieces of code helps to connect to openairealtime with websocket. i need to make a app. i have .wav file i need to send it to openai ai as base64 and receive it as base 64 and save it in my local
# import os
# import json
# import base64
# import asyncio
# import websockets
# from fastapi import FastAPI, WebSocket, Request
# from fastapi.responses import HTMLResponse
# from fastapi.websockets import WebSocketDisconnect
# # from twilio.twiml.voice_response import VoiceResponse, Connect, Say, Stream
# from dotenv import load_dotenv

# # load_dotenv()
# # Load environment variables
# load_dotenv(override=True)
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# # print("OPENAI_API_KEY:", OPENAI_API_KEY)

# # WebSocket URL and headers
# url = "wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview-2024-12-17"
# headers = [
#     "Authorization: Bearer " + OPENAI_API_KEY,
#     "OpenAI-Beta: realtime=v1"
# ]


# # Configuration
# # OPENAI_API_KEY = os.getenv('OPENAI_API_KEY') # requires OpenAI Realtime API Access
# # PORT = int(os.getenv('PORT', 5050))
# # SYSTEM_MESSAGE = (
# #     "You are a helpful and bubbly AI assistant who loves to chat about "
# #     "anything the user is interested in and is prepared to offer them facts. "
# #     "You can start with: Hi, what can I do for you?"
# # )

# SYSTEM_MESSAGE = (
#     "You are a helpful AI assistant"
#     "anything the user is interested in and is prepared to offer them facts. "
#     "You can start with: Hi, what can I do for you?"
# )

# # "You have a penchant for dad jokes, owl jokes, and rickrolling – subtly. "
# # Always stay positive, but work in a joke when appropriate.
# VOICE = 'alloy'
# LOG_EVENT_TYPES = [
#     'response.content.done', 'rate_limits.updated', 'response.done',
#     'input_audio_buffer.committed', 'input_audio_buffer.speech_stopped',
#     'input_audio_buffer.speech_started', 'session.created'
# ]

# app = FastAPI()

# if not OPENAI_API_KEY:
#     raise ValueError('Missing the OpenAI API key. Please set it in the .env file.')


# async def send_to_twilio():
#             """Receive events from the OpenAI Realtime API, send audio back to Twilio."""
#             nonlocal stream_sid
#             try:
#                 async for openai_message in openai_ws:
#                     response = json.loads(openai_message)
#                     if response['type'] in LOG_EVENT_TYPES:
#                         print(f"Received event: {response['type']}", response)
#                     if response['type'] == 'session.updated':
#                         print("Session updated successfully:", response)
#                     if response['type'] == 'input_audio_buffer.speech_started':
#                         await websocket.send_json({ "event": "clear",
#                                                     "streamSid": stream_sid })
#                     if response['type'] == 'response.audio.delta' and response.get('delta'):
#                         # Audio from OpenAI
#                         try:
#                             audio_payload = base64.b64encode(base64.b64decode(response['delta'])).decode('utf-8')
#                             audio_delta = {
#                                 "event": "media",
#                                 "streamSid": stream_sid,
#                                 "media": {
#                                     "payload": audio_payload
#                                 }
#                             }
#                             await websocket.send_json(audio_delta)
#                         except Exception as e:
#                             print(f"Error processing audio data: {e}")
#             except Exception as e:
#                 print(f"Error in send_to_twilio: {e}")

# try:
#     audio_append = {
#                             "type": "input_audio_buffer.append",
#                             "audio": data['media']['payload']
#                         }
#     await openai_ws.send(json.dumps(audio_append))
#     elif data['event'] == 'start':
#     stream_sid = data['start']['streamSid']
#     print(f"Incoming stream has started {stream_sid}")
# except WebSocketDisconnect:
#     print("Client disconnected.")
#     if openai_ws.open:
#         await openai_ws.close()

# async with websockets.connect(
#         'wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview-2024-10-01',
#         extra_headers={
#             "Authorization": f"Bearer {OPENAI_API_KEY}",
#             "OpenAI-Beta": "realtime=v1"
#         }
#     ) as openai_ws:
#         await send_session_update(openai_ws)

# async def send_session_update(openai_ws):
#     """Send session update to OpenAI WebSocket."""
#     session_update = {
#         "type": "session.update",
#         "session": {
#             "turn_detection": {"type": "server_vad"},
#             "input_audio_format": "g711_ulaw",
#             "output_audio_format": "g711_ulaw",
#             "voice": VOICE,
#             "instructions": SYSTEM_MESSAGE,
#             "modalities": ["text", "audio"],
#             "temperature": 0.8,
#         }
#     }
#     print('Sending session update:', json.dumps(session_update))
#     await openai_ws.send(json.dumps(session_update))


import os
import json
import base64
import asyncio
import websockets
from fastapi import FastAPI
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# WebSocket URL and headers
OPENAI_WS_URL = "wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview-2024-12-17"
HEADERS = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "OpenAI-Beta": "realtime=v1"
}

# FastAPI app
app = FastAPI()
import wave

async def send_audio_and_receive_response(wav_file_path: str, output_path: str):
    """Send .wav file as Base64 to OpenAI and save the AI-generated response as .wav"""

    # Read and encode the .wav file
    with open(wav_file_path, "rb") as audio_file:
        audio_base64 = base64.b64encode(audio_file.read()).decode("utf-8")

    async with websockets.connect(OPENAI_WS_URL, additional_headers=HEADERS) as openai_ws:
        print("Connected to OpenAI WebSocket ✅")

        # Send session update
        # session_update = {
        #     "type": "session.update",
        #     "session": {
        #         "output_audio_format": "pcm16",  # Receive PCM16 audio
        #         "modalities": ["audio"],
        #     }
        # }
        # await openai_ws.send(json.dumps(session_update))

        # # Send input audio
        # audio_event = {
        #     "type": "conversation.item.create",
        #     "content": {
        #         "type": []"audio",
        #         "audio": {
        #             "url": "data:audio/wav;base64," + audio_base64
        #         }
        #     }
        # }

        session_update = {
            "type": "session.update",
            "session": {
                "turn_detection": {"type": "server_vad"},
                "input_audio_format": "g711_ulaw",
                "output_audio_format": "g711_ulaw",
                "voice": VOICE,
                "instructions": SYSTEM_MESSAGE,
                "modalities": ["text", "audio"],
                "temperature": 0.8,
            }
        }
        print('Sending session update:', json.dumps(session_update))
        
        # await openai_ws.send(json.dumps(session_update))

        audio_append = {
                            "type": "input_audio_buffer.append",
                            "audio": audio_base64
                        }
        await openai_ws.send(json.dumps(audio_append))
        # await openai_ws.send(json.dumps(audio_event))
        print("Sent audio to OpenAI ✅")

        # Receive response audio and save it
        audio_chunks = []
        audio_bytes = bytearray()
        async for message in openai_ws:
            response = json.loads(message)
            print("Received response:", response)
            
            if response["type"] == "response.audio.delta" and "delta" in response:
                # audio_chunks.append(response["delta"])
                # audio_chunk = base64.b64encode(base64.b64decode(response['delta'])).decode('utf-8')  # Decode each chunk
                audio_chunks.append(response['delta'])
                # audio_bytes.extend(audio_chunk)  # Append to bytearray

            elif response["type"] == "response.done":
                print("Received full response ✅")
                break  # Stop when response is fully received

        # Decode and save the output audio
        if audio_chunks:
            output_audio_base64 = "".join(audio_chunks)
            # txt_file_path = "output.txt"
            # with open(txt_file_path, "wb") as output_file:
            #     # output_audio_bytes = base64.b64decode(output_audio_base64)
            #     output_file.write(output_audio_base64)
            
            output_audio_bytes = base64.b64decode(output_audio_base64)
            

            with wave.open(output_path, "wb") as wav_file:
                wav_file.setnchannels(1)  # Mono
                wav_file.setsampwidth(2)  # 16-bit audio
                wav_file.setframerate(24000)  # Adjust based on your model's settings
                wav_file.writeframes(output_audio_bytes)

            # with open(output_path, "wb") as output_file:
            #     output_file.write(output_audio_bytes)
            print(f"Saved AI-generated audio to {output_path} ✅")

@app.get("/process_audio")
async def process_audio():
    """API Endpoint to send a .wav file and save the AI-generated response"""
    input_wav = "input.wav"   # Change this to your .wav file path
    output_wav = "output.wav" # Change this to your desired output path

    await send_audio_and_receive_response(input_wav, output_wav)
    return {"message": "Audio processing completed!"}