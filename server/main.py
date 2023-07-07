from flask import Flask,request,jsonify,got_request_exception
import time, os
import gpt,user
from werkzeug.utils import secure_filename
import json
import asyncio
import stripe

import random

import openai
import json
import firestore

import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
stripe.api_key = os.environ.get('STRIPE_API_KEY')
endpoint_secret = os.environ.get('STRIPE_ENDPOINT_SECRET')



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
    res = firestore.getRandomTopic(gpt.WritingType)
    return {'topic': res}

@app.route('/getRandomSpeakingTopic')
def route_getRandomSpeakingTopic():
    res = firestore.getRandomTopic(gpt.SpeakingType)
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
    level = user.loginUser(profile)
    return {"level":level}

@app.route('/getUserLevel', methods=['GET'])
def GetUserLevelRoute():
    usr = request.get_json()['user']
    res=user.getUserLevel(usr)
    return {"level": res}

@app.route('/paymentwebhook', methods=['POST'])
def webhook():
    event = None
    payload = request.data

    try:
        event = json.loads(payload)
    except:
        print('⚠️  Webhook error while parsing basic request.' + str(e))
        return jsonify(success=False)
    if endpoint_secret:
        # Only verify the event if there is an endpoint secret defined
        # Otherwise use the basic event deserialized with json
        sig_header = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except stripe.error.SignatureVerificationError as e:
            print('⚠️  Webhook signature verification failed.' + str(e))
            return jsonify(success=False)

    # Handle the even
    if event and event['type'] == 'invoice.payment_succeeded':
        payment_intent = {}
        payment_intent = event['data']['object']  # contains a stripe.PaymentIntent
        print(payment_intent)
        user_email = payment_intent.get('customer_email')
        product_price = payment_intent.get('amount_paid',-1)
        period_start = payment_intent.get('period_start')
        period_end = payment_intent.get('period_end')
        user.updateUserLevelAfterPurchase(str(user_email),product_price,period_start, period_end)
        print(str(user_email)+" -> "+str(product_price))
        print('Payment for {} succeeded'.format(product_price))
        # Then define and call a method to handle the successful payment intent.
        # handle_payment_intent_succeeded(payment_intent)


    elif event['type'] == 'payment_method.attached':
        payment_method = event['data']['object']  # contains a stripe.PaymentMethod
        # Then define and call a method to handle the successful attachment of a PaymentMethod.
        # handle_payment_method_attached(payment_method)
    else:
        # Unexpected event type
        print('Unhandled event type {}'.format(event['type']))

    return jsonify(success=True)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)