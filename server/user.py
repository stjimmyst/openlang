from google.cloud import firestore
import logging


def getUserLevel(username):
    level = 0
    try:
        db = firestore.Client()
        doc = db.collection("users").document(username).get()
        if doc.exists:
            level = doc.get("level")
        logging.debug("request from: " + str(username) + ". level=" + str(level))
    except:
        logging.error("cant init firestore db." )
    return level

def loginUser(profile):
    uid = profile["id"]
    print(uid)
    db = firestore.Client()
    doc = db.collection("users").document(uid).get()
    if doc.exists:
        print("UID="+uid+"already exists")
    else:
        tmp = profile;
        tmp["level"]=1
        db.collection("users").add(tmp,uid)


