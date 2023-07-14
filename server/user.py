import payments
from time import time
from ollogger import OL_logger
from olfirestore import OL_firestore

def updateUserLevelAfterPurchase(email, amount, period_start, period_end):
    OL_logger.info("[updateUserLevelAfterPurchase]. user email: "+email+". purchase: "+ str(amount)+". updating....")
    if (amount==payments.IntermediatePrize):
        level=2
    elif (amount==payments.AdvancedPrize):
        level = 3
    try:
        users_collection = OL_firestore.collection("users")
        users = users_collection.where("email", "==", email).get()
        for u in users:
            doc = users_collection.document(u.id)  # doc is DocumentReference
            field_updates = {"level": level, "period_start": period_start, "period_end": period_end}
            doc.update(field_updates)
            OL_logger.info("[updateUserLevelAfterPurchase]. user email: "+email+". purchase: "+ str(amount)+". updating OK")
    except:
        OL_logger.error("can't update user level after purchase")





def getUserLevel(username):
    level = 0
    OL_logger.debug("Get user level")
    try:
        coll = OL_firestore.collection("users")
        doc = coll.document(username).get()
        if doc.exists:
            period_start = doc.get("period_start")
            period_end = doc.get("period_end")
            current_dt = int(time())
            print("Checking subscription: ["+ str(period_start)+","+str(period_end)+"]. currenttime="+str(current_dt))

            if (current_dt > period_end):
                tmp = coll.document(doc.id)
                tmp.update({"level": 1})
                OL_logger.debug("Subscription expired: setting level=0 for user "+username)
                level = 1
            else:
                level = doc.get("level")

        OL_logger.debug("request from: " + str(username) + ". level=" + str(level))
    except Exception as e:
        print (e)
        OL_logger.error("cant init firestore db." )
    return level

def loginUser(profile):
    uid = profile["id"]
    print(uid)
    doc = OL_firestore.collection("users").document(uid).get()
    if doc.exists:
        print("UID="+uid+"already exists")
        return getUserLevel(uid)
    else:
        tmp = profile;
        tmp["level"]=1
        tmp["period_start"]=0
        tmp["period_end"] = 0
        OL_firestore.collection("users").add(tmp,uid)
        return 0

