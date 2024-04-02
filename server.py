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


@app.route('/speech-to-text', methods=['POST'])
def speech_to_text_route():
    try:
        print("processing speech-to-text")
        audio_binary = request.data # Get user's speech from their request
        text = speech_to_text(audio_binary) # speech transcription 
        
        # Return the response back to the user in JSON format
        response = app.response_class(
            response=json.dumps({'text': text}),
            status=200,  # Set the status to 200 for success
            mimetype='application/json'
        )
        print(response)
        print(response.data)
        return response
    except Exception as e:
        # Handle exceptions and return an appropriate error response
        error_message = "An error occurred while processing the speech: {}".format(str(e))
        response = app.response_class(
            response=json.dumps({'error': error_message}),
            status=500,  # Set the status to 500 for internal server error
            mimetype='application/json'
        )
        return response



@app.route('/process-message', methods=['POST'])
def process_prompt_route():
    response = app.response_class(
        response=json.dumps({"openaiResponseText": None, "openaiResponseSpeech": None}),
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == "__main__":
    app.run(port=8000, host='0.0.0.0')
