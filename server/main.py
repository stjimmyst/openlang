from flask import Flask
import time, os
import mysql.connector

app = Flask(__name__)

mydb = mysql.connector.connect(
  host="35.184.19.133",
  user="root",
  password="Flamingt0rch",
  database="data"
)

def getRandomTopic():
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT topic FROM Topics ORDER BY RAND() LIMIT 1")
    myresult = mycursor.fetchone()
    return myresult["topic"]


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