from flask import Flask,request
import time, os
import mysql.connector
import gpt

app = Flask(__name__)

# mydb = mysql.connector.connect(
#   host="35.184.19.133",
#   user="root",
#   password="Flamingt0rch",
#   database="data"
# )

def getRandomTopic():
    # mycursor = mydb.cursor(dictionary=True)
    # mycursor.execute("SELECT topic FROM Topics ORDER BY RAND() LIMIT 1")
    # myresult = mycursor.fetchone()
    # return myresult["topic"]
    text = """
    An English speaking friend wants to spend a two week holiday in your region and has written
asking for information and advice. Write a letter to your friend, in your letter:
• Offer advice about where to stay
• Give her advice about what to do
• Give information about what clothes to bring
Write at least 150 words. 
    """
    return text

@app.route('/estimateAnswer',methods=["GET"])
def rount_EstimateText():
    question = request.get_json()['question']
    answer = request.get_json()['answer']
    tmp = gpt.estimate_text(question,answer)

    return {'body': tmp}

@app.route('/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/getRandomTopic')
def route_getRandomTopic():
    res = getRandomTopic()
    return {'topic': res}

@app.route('/')
def default_route():
    return {'value':"Hello pridurok"}

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)