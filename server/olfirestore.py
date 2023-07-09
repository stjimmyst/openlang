from google.cloud import firestore
from google.cloud.firestore_v1.collection import CollectionReference
from const import *
from ollogger import *
import time

OL_firestore = firestore.Client()

print("FirestoreDB initialized")

async def OLSaveHistory(username,WritingSpeaking,dict_res):
    col_name = ""
    if (WritingSpeaking == WritingType):
        OL_logger.info("Saving Writing history")
        col_name="writing_history"
    elif (WritingSpeaking == SpeakingType):
        OL_logger.info("Saving Writing history")
        col_name = "speaking_history"
    else:
        OL_logger.error("OLSaveHistory. Wrong type "+ WritingSpeaking)
        return
    col = OL_firestore.collection("users", username, col_name)
    tmp = dict_res
    tmp["timestamp"] = time.time()
    col.add(tmp)



