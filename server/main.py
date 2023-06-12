from flask import Flask,request,got_request_exception
import time, os
import mysql.connector
import gpt

import openai
import json

test_resp = """
{
"criterias": [
{
"comment": "Overall, the response adequately addresses the task requirements and includes all the necessary elements.",
"improvement": "To further improve this criteria, you can provide more specific details about the situation and the potential dangers posed by the dogs.",
"error": "The response could benefit from providing more specific examples or incidents to support the claim of lack of control.",
"band": 6
},
{
"comment": "The response effectively explains why the dogs were a danger to others, highlighting the potential risks and negative impact on safety and well-being.",
"improvement": "To enhance this criteria, you can provide additional examples or specific incidents illustrating the dangers posed by uncontrolled dogs.",
"error": "No significant errors identified.",
"band": 7
},
{
"comment": "The response proposes a solution by suggesting increasing penalties for rule violations and relocating the dog park away from the children's playground.",
"improvement": "To strengthen this criteria, you can provide more detailed justifications for your proposed solutions and consider offering alternative suggestions.",
"error": "No significant errors identified.",
"band": 7
},
{
"comment": "Overall, the response demonstrates sufficient language proficiency with a good range of vocabulary and sentence structures.",
"improvement": "To further improve this criteria, you can vary your sentence structures more, use more advanced vocabulary, and pay attention to grammar and punctuation.",
"error": "Minor errors in punctuation and capitalization (e.g., 'withut' instead of 'without').",
"band": 6
}
]
}
"""
API_KEY = "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"
prompt_template = """analyse my IELTS writing task1 by 4 criterias with score in range 1 to 9. Your response should be in json format {format}. Per each critera provide:
comment: detalaied answer and expalanation
improvements: how can  improve this criteria?
errors: example of errors in essay.
band: you estimated band by criteria

TASK:
{task}
RESPONSE:
{response}
"""
task = """
You recently visited a dog park and were disturbed by the lack of control the owners
imposed on their dogs, making them dangerous for everyone around.

Write an email to your local municipality in about 150-200
words. Your email should include the following things:
• Describe the situation
• Explain why the dogs were a danger to others
• Propose a solution
"""
response = """
Dear local municipality,
The main purpose of my writing today is to lodge a complaint about the dog park in our town, that I visited with my family last weekend.
To begin with, I was playing with my kids when a gigantic dog without a leash
suddenly appeared behind my back. 
My kids were very scared by this aggressive barking creature and started crying.
It's very important to respect the rule of each and other in our society. 
Big creatures like this dog, walking around the park withut control, may be not only a source of danger but also a cause of various viruses for humans.
Based on what I have provided you today, I may suggest a few options to solve this problem. 
Firstly, I would strongly recommend increasing the amount of penalty for breaking the rules in our park. Furthermore, it will be a good idea to move the dog park far away from the children's playground.
I am looking forward to seeing how my suggestions translate to prompt actions from your side.
Your kind cooperation would be most appreciated.
Sincerely,
Alexey Ivanov.
"""

format="""{criterias:[{comment, improvement, error, band}]}"""

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

    esse = json.loads(test_resp)
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

@app.route('/')
def default_route():
    return {'value':"Hello pridurok"}

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)