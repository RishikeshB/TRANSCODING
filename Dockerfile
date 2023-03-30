#dockerfile,image,container
FROM python:3.9-slim

COPY requirements.txt .
RUN pip install -r requirements.txt
ADD main.py . 
ADD source ./source
ADD /var ./var
# RUN pip install ffmpeg-python
RUN apt-get -y update && apt-get install -y ffmpeg libsm6 libxext6 -y
# RUN pip install python-ffmpeg-video-streaming
# RUN pip install azure-storage-blob
CMD ["python","./main.py"]