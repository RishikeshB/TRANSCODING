import ffmpeg_streaming
from ffmpeg_streaming import Formats, Bitrate, Representation, Size
import os
import logging
logger=logging.getLogger("transcoder")
# pip install azure-storage-blob
from azure.storage.blob import BlobServiceClient
def video_Transcoding():
    path='source/video.mp4'
    logger.info(os.path.isfile(path))
    video = ffmpeg_streaming.input(path)
    #pixel Size=Represention(Size(pixel length*pixel height),Bitrate(upload bitrate,download bitrate))
    _144p = Representation(Size(256, 144), Bitrate(95 * 1024, 64 * 1024))
    _240p = Representation(Size(426, 240), Bitrate(150 * 1024, 94 * 1024))
    _360p = Representation(Size(640, 360), Bitrate(276 * 1024, 128 * 1024))
    _480p = Representation(Size(854, 480), Bitrate(750 * 1024, 192 * 1024))
    _720p = Representation(Size(1280, 720), Bitrate(2048 * 1024, 320 * 1024))
    hls = video.hls(Formats.h264())
    hls.representations(_144p,_240p, _360p, _480p, _720p) 
    # _240p, _360p, _480p, _720p
    hls.output('./var/media/hls.m3u8')
    logger.info("transcoding completed.....")
def upload_Azure():
    storage_connection_string='DefaultEndpointsProtocol=https;AccountName=blobcontainerforlive;AccountKey=04BtCVQUVYi0/XOEIQmsKe/U7ShQ7ujEJ24WGYBOGYkjuy2EmHIqYiVV/1KC5GLnl3B9rnnj5MAc+AStrv5nhg==;EndpointSuffix=core.windows.net'
    blob_service_client=BlobServiceClient.from_connection_string(storage_connection_string)
    container_name="live007"
    container_client=blob_service_client.get_container_client(container_name)
    if not container_client.exists():
        logger.info("container does not exit...creating it")
        blob_service_client.create_container(container_name)
        # blob_service_client.set_blob_acl(container_name, public_access=PublicAccess.Blob)
    file_folder='./var/media'
    for file_name in os.listdir(file_folder):
        blob_obj=blob_service_client.get_blob_client(container=container_name,blob=file_name)
        logger.info(f'Uploading file:{file_name}...')
        with open(os.path.join(file_folder,file_name),mode='rb')as file_data:
            blob_obj.upload_blob(file_data)

if __name__=="__main__":
    logger.info("Transcoding....")
    video_Transcoding()
    logger.info("uploading to azure....")
    upload_Azure()
    logger.info("uploading completed....")
   