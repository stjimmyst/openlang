import logging

from google.cloud import firestore
import random
import gpt

defaultSpeakingTopic = """Describe a house or apartment you would like to live in.
    You should say:
    • where it is / Where it would be
    • what you would (like to) do there
    • who you would (like to) live therewith
    • and explain why you would like to live in this place."""

defaultWritingTopic = """An English speaking friend wants to spend a two week holiday in your region and has written
asking for information and advice. Write a letter to your friend, in your letter:
• Offer advice about where to stay
• Give her advice about what to do
• Give information about what clothes to bring
Write at least 150 words. 
    """

IeltsSpeakingCollection = "ielts_speaking"
IeltsWritingCollection = "ielts_writing"
def getRandomTopic(type):
    if (type==gpt.SpeakingType):
        collection=IeltsSpeakingCollection
        topic = defaultSpeakingTopic;
    else:
        collection=IeltsWritingCollection
        topic = defaultWritingTopic;

    db = firestore.Client()
    number = 0
    doc = db.collection(collection+"_count").document("count").get()
    if doc.exists:
        number = doc.get("count")
        logging.debug("collection count = "+ str(number))
        random_topic = random.randint(0,number-1)
        print(random_topic)
        topics = db.collection(collection).where("id","==",random_topic).stream()
        for t in topics:

            topic = t.get("topic")
            print(topic)
    return topic.replace("\\n", "\n");