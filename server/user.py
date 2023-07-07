from google.cloud import firestore
import logging
import payments
from time import time

def updateUserLevelAfterPurchase(email, amount, period_start, period_end):
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
            field_updates = {"level": level, "period_start": period_start, "period_end": period_end}
            doc.update(field_updates)
            logging.info("[updateUserLevelAfterPurchase]. user email: "+email+". purchase: "+ str(amount)+". updating OK")
    except:
        logging.error("can't update user level after purchase")





def getUserLevel(username):
    level = 0
    logging.debug("Get user level")
    try:
        db = firestore.Client()
        coll = db.collection("users")
        doc = coll.document(username).get()
        if doc.exists:
            #check subscription
            period_start = doc.get("period_start")
            period_end = doc.get("period_end")
            current_dt = int(time())
            print("Checking subscription: ["+ str(period_start)+","+str(period_end)+"]. currenttime="+str(current_dt))

            if (current_dt > period_end):
                tmp = coll.document(doc.id)
                tmp.update({"level": 0})
                logging.debug("Subscription expired: setting level=0 for user "+username)
                level = 0
            else:
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
        return getUserLevel(uid)
    else:
        tmp = profile;
        tmp["level"]=0
        tmp["period_start"]=0
        tmp["period_end"] = 0
        db.collection("users").add(tmp,uid)
        return 0


