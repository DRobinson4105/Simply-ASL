from flask import Flask, request, jsonify, send_file
from utils import *
import numpy as np

app = Flask(__name__)

@app.route('/receive-text', methods=['POST'])
def receive_text():
    # Get the recognized text from the request
    data = request.get_json()
    recognized_text = data.get('recognizedText')

    # Check if recognized text is present
    if not recognized_text:
        return jsonify({"error": "No text provided"}), 400

    # Convert recognized text to ASL gloss
    try:
        gloss = text2gloss(recognized_text)
        pose1 = gloss2pose(gloss)
        pose2 = np.array(intermediatePose(pose1))

        return jsonify({"message": "Text processed successfully", "text": recognized_text, "gloss": gloss})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/video')
def stream_video():
    return send_file('../dataset/ABANDON.mp4', mimetype='video/mp4')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
