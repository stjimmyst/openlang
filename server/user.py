from google.cloud import firestore
import logging
import payments

def updateUserLevelAfterPurchase(email, amount):
    logging.info("[updateUserLevelAfterPurchase]. user email: "+email+". purchase: "+ str(amount)+". updating....")
    if (amount==payments.IntermediatePrize):
        level=1
    elif (amount==payments.AdvancedPrize):
        level = 2
    try:
        db = firestore.Client()
        users_collection = db.collection("users")
        users = users_collection.where("email", "==", email).get()
        for u in users:
            doc = users_collection.document(u.id)  # doc is DocumentReference
            field_updates = {"level": level}
            doc.update(field_updates)
            logging.info("[updateUserLevelAfterPurchase]. user email: "+email+". purchase: "+ str(amount)+". updating OK")
    except:
        logging.error("can't update user level after purchase")




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
        return doc.get("level")
    else:
        tmp = profile;
        tmp["level"]=0
        db.collection("users").add(tmp,uid)
        return 0


