from flask import Flask, request, jsonify, send_file
from utils import *
import numpy as np
import time

app = Flask(__name__)

@app.route('/process', methods=['POST'])
async def receive_text():
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
        
        # Turn pose2 into a video and save it
        output_video_path = 'output.mp4'  # Save the video in a directory
        pose2video(pose2)  # Assuming pose2video saves the video

        # Return the video file as a response
        if os.path.exists(output_video_path):
            return send_file(output_video_path, mimetype='video/mp4')
        else:
            return jsonify({"error": "Video file not found"}), 500
    except Exception as e:
        print("Error processing ASL gloss:", e)
        return jsonify({"error": str(e)}), 500
    
    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
