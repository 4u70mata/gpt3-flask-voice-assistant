import base64
import json
from flask import Flask, render_template, request
from worker import speech_to_text, text_to_speech, openai_process_message
from flask_cors import CORS
import os

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# End-point for converting user's speech to text
@app.route('/speech-to-text', methods=['POST'])
def speech_to_text_route():
    print("processing speech-to-text")
    audio_binary = request.data # get user's speech from their request
    text = speech_to_text(audio_binary)

    # Return the response back to the user is JSON format
    response = app.response_class(
        response = json.dumps({'text': text}),
        status=200,
        mimetype='application/json'
    )
    # del after debuging
    print(response)
    print(response.data)


    return response


# End-point for processing user's message and converting OpenAI's response to speech
@app.route('/process-message', methods=['POST'])
def process_message_route():
    user_message = request.json['userMessage'] # Get user message from request json 
    print('use_message', user_message)

    voice = request.json['voice'] # get use voice if selected
    # Open Ai process message
    openai_response_text = openai_process_message(user_message)
    # removing the empy lines ( fasle lines '')
    openai_response_text = os.linesep.join([s for s in openai_response_text.splitlines() if s])
    # call the TTS worker function with voice if wanted : 
    openai_response_speech = text_to_speech(openai_response_text, voice)
    # Convert speech data to Base64 encoding for JSON response
    openai_response_speech = base64.b64encode(openai_response_speech).decode('utf-8')


    response = app.response_class(
        response=json.dumps({"openaiResponseText": openai_response_text, "openaiResponseSpeech": openai_response_speech}),
        status=200,
        mimetype='application/json'
    )
    print(response)
    return response


if __name__ == "__main__":
    app.run(port=8000, host='0.0.0.0')
