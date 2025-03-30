#!/usr/bin/env python3
import os
import subprocess
from flask import Flask, request, jsonify
from gtts import gTTS

app = Flask(__name__)

# Define valid buttons: numbers 0-9, plus "c" and "ent"
ALLOWED_BUTTONS = [str(i) for i in range(0, 10)] + ["c", "ent"]

# Directory to store audio files
AUDIO_DIR = "audio_files"
if not os.path.exists(AUDIO_DIR):
    os.makedirs(AUDIO_DIR)

def generate_tts(text, button):
    """
    Generate a TTS audio file using gTTS for the given text and save it as '<button>.mp3'.
    """
    tts = gTTS(text)
    filename = os.path.join(AUDIO_DIR, f"{button}.mp3")
    tts.save(filename)
    return filename

def play_audio(file_path):
    """
    Play the specified audio file using VLC's command-line interface (cvlc).
    """
    subprocess.Popen(
        ["cvlc", "--play-and-exit", "--gain", "1.25", file_path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

# Initialize audio files for each button with the default message "playing button {button}"
for button in ALLOWED_BUTTONS:
    filename = os.path.join(AUDIO_DIR, f"{button}.mp3")
    if not os.path.exists(filename):
        generate_tts(f"playing button {button}", button)

@app.route("/<button>", methods=["GET"])
def play_button(button):
    """
    On a GET request to /<button>, play the audio file assigned to that button.
    """
    if button not in ALLOWED_BUTTONS:
        return jsonify({"error": "Invalid button"}), 400
    filename = os.path.join(AUDIO_DIR, f"{button}.mp3")
    if os.path.exists(filename):
        play_audio(filename)
        return jsonify({"status": "playing", "button": button})
    return jsonify({"error": "Audio file not found"}), 404

@app.route("/<button>/edit", methods=["POST"])
def edit_button(button):
    """
    On a POST request to /<button>/edit with JSON { "message": "<new message>" },
    update the audio file by generating new text-to-speech audio.
    """
    if button not in ALLOWED_BUTTONS:
        return jsonify({"error": "Invalid button"}), 400
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Invalid data. Provide a JSON with a 'message' key."}), 400
    new_message = data["message"]
    generate_tts(new_message, button)
    return jsonify({"status": "updated", "button": button, "new_message": new_message})

if __name__ == "__main__":
    # The server listens on all interfaces at port 5000
    app.run(host="0.0.0.0", port=5000, debug=True)

