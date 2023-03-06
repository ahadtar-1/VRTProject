FROM python:3.8

WORKDIR /app

COPY . /app

RUN apt update
RUN apt install -y libgl1-mesa-glx
RUN pip install -r requirements.txt

#EXPOSE 5000

ENTRYPOINT ["python"]
CMD ["app.py"]