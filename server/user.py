from google.cloud import firestore


def getUserLevel(username):
    print("get response from")
    print(username)
    level = 0
    db = firestore.Client()
    doc = db.collection("users").document(username).get()
    if doc.exists:
        level = doc.get("level")
    print(level)
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


