from flask import Flask,request,got_request_exception
import time, os
import gpt,user
from werkzeug.utils import secure_filename
import asyncio

import random

import openai
import json

import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)


def getRandomSpeakingTopic():
    text = """Describe a house or apartment you would like to live in.
You should say:
• where it is / Where it would be
• what you would (like to) do there
• who you would (like to) live therewith
• and explain why you would like to live in this place."""
    return text
def getRandomTopic():
    # mycursor = mydb.cursor(dictionary=True)
    # mycursor.execute("SELECT topic FROM Topics ORDER BY RAND() LIMIT 1")
    # myresult = mycursor.fetchone()
    # return myresult["topic"]
    text = """An English speaking friend wants to spend a two week holiday in your region and has written
asking for information and advice. Write a letter to your friend, in your letter:
• Offer advice about where to stay
• Give her advice about what to do
• Give information about what clothes to bring
Write at least 150 words. 
    """
    return text

@app.route('/estimateSpeakingTest',methods=["GET","POST"])
def routeEstimateSpeakingTest():
    f = request.files["file"]
    question = json.loads(request.form.get('question'))['question']
    return {'body':{
        'transcription': "testing transcription from the server",
        'fc':
            {
                            'comment':"Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.",
                            'band': random.randint(1,9)
            },
        'gra':
            {
                'comment': "comment2",
                'band': random.randint(1, 9)
            },
        'lr':
            {
                'comment': "comment3",
                'band': random.randint(1, 9)
            },
        'p':
            {
                'comment': "comment4",
                'band': random.randint(1, 9)
            }
                    }
            }
@app.route('/estimateWritingTest',methods=["GET","POST"])
def routeEstimateWritingTest():
    question = request.get_json()['question']
    answer = request.get_json()['answer']
    return {'body':{
        'ta':
            {
                            'comment':"Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.",
                            'band': random.randint(1,9)
            },
        'gra':
            {
                'comment': "comment2",
                'band': random.randint(1, 9)
            },
        'lr':
            {
                'comment': "comment3",
                'band': random.randint(1, 9)
            },
        'cc':
            {
                'comment': "comment4",
                'band': random.randint(1, 9)
            }
                    }
            }


@app.route('/estimateAnswer',methods=["GET","POST"])
def rount_EstimateText():
    # try:
    question = request.get_json()['question']
    answer = request.get_json()['answer']

        # openai.api_key = API_KEY
        # prompt = prompt_template.format(task=task, response=response, format=format)
        # print(prompt)
        # completion = openai.ChatCompletion.create(
        #     model="gpt-3.5-turbo",
        #     messages=[
        #         {"role": "user",
        #          "content": "say hello!"}
        #     ]
        # )
        # tmp = completion.choices[0].message["content"]
        # print(tmp)
    #gpt.estimate_text(question,answer)
    esse = json.loads(gpt.estimate_text(question,answer))
    print(esse)
    return {'body': esse}
    # except Exception as e:
    #     return {
    #         'request': str(request.data),
    #         'body': str(e)}

@app.route('/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/getRandomTopic')
def route_getRandomTopic():
    res = getRandomTopic()
    return {'topic': res}

@app.route('/getRandomSpeakingTopic')
def route_getRandomSpeakingTopic():
    res = getRandomSpeakingTopic()
    return {'topic': res}

@app.route('/')
def default_route():
    return {'value':"Hello pridurok"}

@app.route('/WritingEstimation',methods=["GET","POST"])
async def WritingEstimationRoute():
    question = request.get_json()['question']
    answer = request.get_json()['answer']
    user = request.get_json()['user']
    # res = await gpt.WritingEstimationChatModel(question,answer)
    res = await gpt.WritingEstimationChat(question, answer,user,gpt.WritingType)
    return {'body':res}

@app.route("/SpeakingEstimation",methods=["GET","POST"])
async def SpeakingEstimationRoute():
    if request.files.get("file") is None:
        return {'failed': 'OK'}
    f = request.files["file"]
    params = json.loads(request.form.get('params'));
    question = params['question']
    user = params['user']
    f.save(secure_filename(f.filename))
    answer = gpt.voiceToText("audiofile.mp3")
    res = await gpt.WritingEstimationChat(question, answer, user, gpt.SpeakingType)
    return {'transcription':answer, 'body':res}


@app.route("/login",methods=["POST"])
def LoginRoute():
    profile = request.get_json()['profile']
    print(profile)
    user.loginUser(profile)
    return {"response":"OK"}


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
    logging.debug("some message")
    app.logger.debug("debug log info")
    app.logger.info("Info log information")
    app.logger.warning("Warning log info")
    app.logger.error("Error log info")
    app.logger.critical("Critical log info")