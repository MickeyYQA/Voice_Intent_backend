import os

from flask import Flask, request, jsonify

from audio_emotions import analyze_emotion_from_audio
from pragmatic_figurative_language_classifier import analyze_pragmatic_language
from pragmatic_figurative_language_classifier import analyze_literal_vs_figurative

app = Flask(__name__)
os.makedirs("uploads", exist_ok=True)

@app.route("/audio-prosody", methods = ["POST"])
def audio_prosody():
    if "file" not in request.files:
        return jsonify({"error": "Missing file"}), 400
    
    file = request.files['file']
    file_path = os.path.join("uploads", file.filename)
    file.save(file_path)

    try:
        result = analyze_emotion_from_audio(file_path)
        print(result)
        return jsonify(result)
    finally:
        os.remove(file_path)
    
@app.route("/pragmatic", methods = ["POST"])
def pragmatic():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Missing 'text' field"}), 400
    text = data ["text"]
    result = analyze_pragmatic_language(text)
    return jsonify(result)

@app.route("/literal", methods = ["POST"])
def literal():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Missing 'text' field"}), 400
    
    text = data["text"]
    result = analyze_literal_vs_figurative(text)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 1234)