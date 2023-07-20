import os

from google.cloud import storage
from ollogger import OL_logger

OL_filestorage = storage.Client()

print("Google cloud storage initialized")

async def OLSaveAudio(username, uuid,test_type):

    try:
        print("saving audio")
        bucket = OL_filestorage.get_bucket('openlang')
        blob = bucket.blob('speaking/' + username + '/'+test_type+"/"+uuid+".mp3")
        blob.upload_from_filename(uuid+".mp3")
        os.remove(uuid+".mp3")
    except Exception as e:
        print(str(e))
        OL_logger.error("OLSaveHistory: " + str(e))




