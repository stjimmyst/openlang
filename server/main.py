from flask import Flask, request, jsonify, got_request_exception
import time, os
import gpt, user
from werkzeug.utils import secure_filename
import json
import asyncio
import stripe
import uuid

import random

import openai
import json
import topics

from ollogger import OL_logger, RequestLog
from olfirestore import OLSaveHistory,OL_firestore
from olfilestorage import OLSaveAudio
from const import *

app = Flask(__name__)

stripe.api_key = os.environ.get('STRIPE_API_KEY')
endpoint_secret = os.environ.get('STRIPE_ENDPOINT_SECRET')


@app.route('/estimateSpeakingTest', methods=["GET", "POST"])
def routeEstimateSpeakingTest():
    f = request.files["file"]
    question = json.loads(request.form.get('question'))['question']
    return {'body': {
        'transcription': "testing transcription from the server",
        'fc':
            {
                'comment': "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.",
                'band': random.randint(1, 9)
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


@app.route('/estimateWritingTest', methods=["GET", "POST"])
def routeEstimateWritingTest():
    question = request.get_json()['question']
    answer = request.get_json()['answer']
    return {'body': {
        'ta':
            {
                'comment': "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.",
                'band': random.randint(1, 9)
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


@app.route('/estimateAnswer', methods=["GET", "POST"])
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
    # gpt.estimate_text(question,answer)
    esse = json.loads(gpt.estimate_text(question, answer))
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
    test_type = request.args['test_type']
    task_type = request.args['task_type']
    res = topics.getRandomTopic(task_type,test_type)
    return {'topic': res}


@app.route('/')
def default_route():
    return {'value': "Hello pridurok"}


@app.route('/WritingEstimation', methods=["GET", "POST"])
async def WritingEstimationRoute():
    if request.get_json()['question'] is None:
        return {'failed': 'no question field'}
    question = request.get_json()['question']
    answer = request.get_json()['answer']
    user = request.get_json()['user']
    test_type = request.get_json()['test']
    request_uuid = str(uuid.uuid4())
    res = await gpt.WritingEstimationChat(question, answer, user, WritingType,test_type)
    tmp = {'question': question, 'results': res, 'answer': answer, 'test_type': test_type}
    asyncio.create_task(OLSaveHistory(user, WritingType, tmp, request_uuid,test_type))
    return tmp

@app.route("/ReadingEstimation", methods=["POST"])
async def ReadingEstimationRoute():
    body = request.get_json()
    if body is None:
        return {'failed': 'no json received'}
    test_type = body['test_type']
    test_id = body['test_id']
    inputuser = request.get_json()['user']
    answers = body['answers']
    level = user.getUserLevel(inputuser)
    question_definition = OL_firestore.collection(test_type+"_reading").document(test_id).get().to_dict()
    errors = []
    for question in question_definition['plain-answers']:
        safe_answer = answers.get(question['item_uuid'], "")
        if question['answer'] != safe_answer:
            tmp_explain = ""
            if level < 2:
                tmp_explain = "Explanations are not available in your subscription plan"
            else:
                tmp_explain = question['item_explanation']
            tmp = {
                "id": question['item_number'],
                "correct_answer": question['answer'],
                "explanation": tmp_explain
            }
            errors.append(tmp)
    number_errors = len(errors)
    overall = ""
    if number_errors == 0:
        overall = "9.0"
    elif (number_errors==1):
        overall = "8.5"
    elif ((number_errors>=2) and (number_errors <=3)):
        overall = "8.0"
    elif (number_errors == 4):
        overall = "7.5"
    elif (number_errors>=5 and number_errors <=6):
        overall = "7.0"
    elif (number_errors>=7 and number_errors <=8):
        overall = "6.5"
    elif (number_errors>=9 and number_errors <=10):
        overall = "6.0"
    elif (number_errors>=11 and number_errors <=13):
        overall = "5.5"
    elif (number_errors>=14 and number_errors <=17):
        overall = "5.0"
    elif (number_errors>=18 and number_errors <=21):
        overall = "4.5"
    elif (number_errors>=22 and number_errors <=25):
        overall = "4.0"
    else:
        overall = "< 4.0"

    tmp_res = {"id": test_id, "score": overall, "errors": errors, "level": level}
    history_res = tmp_res
    history_res['answers'] = answers
    asyncio.create_task(OLSaveHistory(inputuser, ReadingType, history_res, str(uuid.uuid4()), test_type))

    return tmp_res

@app.route("/SpeakingEstimation", methods=["GET", "POST"])
async def SpeakingEstimationRoute():
    if request.files.get("file") is None:
        return {'failed': 'no file recieved'}
    if request.form.get('params') is None:
        return {'failed': 'no params josn'}
    f = request.files["file"]
    params = json.loads(request.form.get('params'));
    question = params['question']
    user = params['user']
    test_type = params['test']
    request_uuid = str(uuid.uuid4())
    f.save(secure_filename(request_uuid + ".mp3"))
    answer = gpt.voiceToText(request_uuid + ".mp3")
    res = await gpt.WritingEstimationChat(question, answer, user, SpeakingType, test_type)
    tmp = {'question': question, 'transcription': answer, 'results': res, 'test_type': test_type}
    asyncio.create_task(OLSaveHistory(user, SpeakingType, tmp, request_uuid,test_type))
    asyncio.create_task(OLSaveAudio(user, request_uuid,test_type))
    return tmp


@app.route("/login", methods=["POST"])
def LoginRoute():
    print(request.json)
    RequestLog("/login", request.json)
    profile = request.get_json()['profile']
    level = user.loginUser(profile)
    return {"level": level}


@app.route('/getUserLevel', methods=['GET'])
def GetUserLevelRoute():
    usr = request.get_json()['user']
    res = user.getUserLevel(usr)
    return {"level": res}


@app.route('/paymentwebhook', methods=['POST'])
def webhook():
    event = None
    payload = request.data

    try:
        event = json.loads(payload)
    except Exception as e:
        print('⚠️  Webhook error while parsing basic request.' + str(e))
        return jsonify(success=False, error=str(e), body=payload,msg="cannoot processed json.loads")
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
            return jsonify(success=False, error=str(e), type='Webhook signature verification failed')

    # Handle the even
    if event and event['type'] == 'invoice.payment_succeeded':
        payment_intent = {}
        payment_intent = event['data']['object']  # contains a stripe.PaymentIntent
        OL_logger.error("[PAYMENT] ")
        print("[PAYMENT]" + str(payment_intent))
        user_email = payment_intent.get('customer_email')
        # product_price = payment_intent.get('amount_paid', -1)
        product_price=1499
        period = event['data']['object']['lines']['data'][0]['period']
        period_start = period.get("start")
        period_end = period.get("end")
        user.updateUserLevelAfterPurchase(str(user_email), product_price, period_start, period_end)
        OL_logger.debug(str(user_email) + " -> " + str(product_price))
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
    OL_logger.info("Flask server started")
    app.run(debug=True, host='0.0.0.0', port=port)
