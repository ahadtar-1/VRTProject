"""
The module comprises of the video superresolution API
"""

from flask import Flask, request, send_file, jsonify, render_template
import base64
import os
from operations import video_superresolution
from flask_ngrok import run_with_ngrok

app = Flask(__name__, template_folder = 'templates')
uploadsDir = ""
run_with_ngrok(app)


@app.route("/")
def home():
    """
    The api function that displays the home page

    Parameters
    ----------
    None

    Returns
    -------
    None

    """
    
    return render_template('page.html')


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
            #file = request.files['file']
            #if file.filename == '':
            #    raise Exception('No file sent')
            #if not file.filename.lower().endswith(('.mp4', '.avi', '.mkv')):
            #    raise Exception("Invalid file type")
            #fileName = file.filename
            #file.save(os.path.join(uploadsDir, fileName))
            #path = video_superresolution(os.path.join(uploadsDir, fileName))
            #return send_file(path)
        #except Exception as e:
            #return f'An error occurred: {str(e)}'
            
            videoBase64 = request.json.get("videoBase64")
            if not videoBase64:
                raise ValueError("No video data received.")        
            videoData = base64.b64decode(videoBase64)
            fileExtension = request.json.get("fileExtension")                        
            if not fileExtension:
                raise ValueError("No file extension.")            
            if fileExtension not in [".mp4", ".mkv", ".avi"]:
                raise ValueError("Invalid file extension, only mp4, avi, and mkv files are accepted.")
            
            with open(os.path.join(uploadsDir, f"new_video{fileExtension}"), "wb") as video_file:
                video_file.write(videoData)
                path = video_superresolution(os.path.join(uploadsDir, f"new_video{fileExtension}"))
                print("Video sent to model successfully")
                return send_file(path)                    
        
        except Exception as e:
            return jsonify({"message": f"Error: {e}"}), 400
        
        #try:
        #    f = request.files['file']
        #    if not f.filename.lower().endswith(('.mp4', '.avi', '.mkv')):
        #        raise ValueError("Invalid file type")
        #except KeyError:
        #    return "Incorrect key sent with file", 400
        #except ValueError as e:
        #    return (f'Error: {str(e)}')
        
        #fileName = f.filename
        #f.save(os.path.join(uploadsDir, fileName))
        #path = video_superresolution(os.path.join(uploadsDir, fileName))
        #return send_file(path)
