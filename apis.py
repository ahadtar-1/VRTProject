"""
The module comprises of the different APIs
"""

from flask import Flask, request, send_file
import os
from operations import video_superresolution

app = Flask(__name__)
uploadsDir = "/home/ekkelai/Documents/VRT/videos/"


@app.route("/")
def home():
    return "<h1>The Dockerised flask application is working</h1>"


@app.route('/videosuperresolution', methods = ['GET', 'POST'])
def superresolution_video()-> str:
    """
    The api function that generates an super resolution video from a video.

    Parameters
    ----------
    None
    
    Returns
    -------
    str
    
    """
            
    if request.method == 'POST':
        try:
            f = request.files['file']
            if not f.filename.lower().endswith(('.mp4', '.avi', '.mkv')):
                raise ValueError("Invalid file type")
        except KeyError:
            return "Incorrect key sent with file", 400
        except ValueError as e:
            return (f'Error: {str(e)}')
        
        fileName = f.filename
        f.save(os.path.join(uploadsDir, fileName))
        path = video_superresolution(os.path.join(uploadsDir, fileName))
        return send_file(path)
