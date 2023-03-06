# VRTProject

This project implements a VRT(Video Restoration Transformer) for the purpose of performing superresolution on videos. The whole project is built in a dockerized environment.

# Set up and Installation

### Case 1 - Run Project using Docker Image

The docker image required for this project is available on Docker hub and can be pulled. The project will be up and running once it is pulled and the command to run the docker container is entered.

```bash
git clone https://github.com/ahadtar-1/VRTProject.git

cd VRTProject

docker pull ahadtar1/vrtflask_dockerapp:latest

docker run -it ahadtar1/vrtflask_dockerapp:latest
```

### Case 2 - Build Docker Image and Run Project

The docker file is provided in the project which builds an image. The project will be up and running once the commands for building the image and container are entered.

```bash
docker build -t ahadtar1/vrtflask_dockerapp:latest . 
```

```bash
docker run -it ahadtar1/vrtflask_dockerapp:latest
```

### Case 3 - Run Project without Docker

The project can be run in a non dockerized environment. For that purpose a conda environment should be created (**VRTProject**) to preserve the existant packages and dependencies in the system. The requirements file should then be run in the environment to import the required dependencies for the project. Once packages are imported the project can be run.

```bash
conda create --name VRTProject python=3.8

source activate VRTProject

pip install -r requirements.txt
```

```bash
python3 app.py
```

# APIs

### Video Superresolution

A post request would be sent to the flask server. It would comprise of a video file. The response sent back from the server would be a superresolution  mp4 video file of the sent video. The accepted video file formats are only mp4, avi, and mkv.

#### API Endpoint

```
127.0.0.1:5000/videosuperresolution 
```

#### Payload
```
{
    "file" : testvideo.mp4

    key must be the string "file"
    value must be an mp4 video file
}
```
