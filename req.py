import base64
import requests

fileName = "videoblockhyderabads-short-clip-of-information-and-reservation-office--outside-board_hpfio1hdv__9c649df08ac08f7aeaba562d40b44ce1__P360.mp4"
with open(fileName, "rb") as video_file:
    videoData = video_file.read()

videoBase64 = base64.b64encode(videoData).decode("utf-8")
url ="http://bc02-35-233-171-254.ngrok.io/videosuperresolution"

data = {"videoBase64": videoBase64, "fileExtension": f".{fileName.split('.')[-1]}"}
session = requests.Session()
response = session.post(url, json=data)
#response = requests.post(url, json=data)

if response.status_code == 200:
    print("Video uploading success!")
else:
    print("Video uploading failed")
