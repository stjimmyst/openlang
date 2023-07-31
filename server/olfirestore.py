from google.cloud import firestore
from google.cloud.firestore_v1.collection import CollectionReference
from const import *
from ollogger import *
import time

OL_firestore = firestore.Client()

print("FirestoreDB initialized")

async def OLSaveHistory(username,WritingSpeaking,dict_res,uuid,test_type):
    col_name = ""
    if (WritingSpeaking == WritingType):
        OL_logger.info("Saving Writing history")
        col_name=test_type+"_writing_history"
    elif (WritingSpeaking == SpeakingType):
        OL_logger.info("Saving Writing history")
        col_name = test_type+"_speaking_history"
    elif (WritingSpeaking == ReadingType):
        OL_logger.info("Saving Reading history")
        col_name = test_type+"_reading_history"
    else:
        OL_logger.error("OLSaveHistory. Wrong type "+ WritingSpeaking)
        return
    try:
        col = OL_firestore.collection("users", username,col_name)
        tmp = dict_res
        tmp["timestamp"] = time.time()
        col.add(tmp,uuid)
    except Exception as e:
        print("Can't save History to firestore "+str(e))
        OL_logger.error("OLSaveHistory: " + str(e))



