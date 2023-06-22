import openai
import os
import json


# API_KEY = "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"
openai.api_key = "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"
prompt_template_speaking = """
analyse my IELTS speaking (transcription) by 4 criterias with score in range 1 to 9 Your response should be in json format {format}. Per each critera provide:
comment: detalaied answer and expalanation
improvements: how can  improve this criteria?
errors: example of errors in essay.
band: you estimated band by criteria.

TASK:
{task}
RESPONSE:
{response}
"""
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
speaking_format="""fc,lr,gra,p."""
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

format="""ta,cc,lr,gra. Eacch category is {comment, error, band}"""

def voiceToText(filename):
    if True:
        audio_file = open(filename, "rb")
        # resp = openai.Audio.transcribe("whisper-1", audio_file)
        resp = openai.Audio.translate("whisper-1", audio_file)
        print(resp)
        tmp = resp['text']
        print(tmp)
        return tmp
    else:
        print( "please set environment variable")
def estimate_text(question, answer):
    #os.environ["OPENAI_API_KEY"] = API_KEY
    prompt = prompt_template.format(task=question,response=answer,format=format)
    print(prompt)
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user",
             "content": prompt}
        ]
    )
    tmp = completion.choices[0].message["content"]
    print(tmp)
    return tmp


testestimator = """
{
 "fc": {
    "comment": "The response fulfills all the requirements of the task and covers all parts of the prompt in a logical order. The speaker states the location and the activities they wish to perform in the apartment, which is suitable for dwelling with a family member or a close friend. Additionally, the explanation of why this place is desirable is well-supported and coherent. ",
    "improvements": "To improve, the speaker could aim to use more complex sentence structures and improve their range of vocabulary.",
    "errors": [],
    "band": 8
 },
 "lr": {
    "comment": "The speaker kept speaking fluently without any pauses, and responded promptly to the task prompt. However, there are a few instances where there are pauses and repetition of some words or ideas.",
    "improvements": "To improve, the speaker could practise using connectors and transition words that will help keep the pace of the speech constant. This would also help reduce repeating their words or ideas.",
    "errors": [],
    "band": 7
 },
 "gra": {
    "comment": "The response is grammatically correct, and the speaker's use of tenses is consistent throughout the monologue. There are only a few minor syntactical errors but they do not affect meaning.",
    "improvements": "To improve, the speaker can aim to incorporate more complex sentence structures.",
    "errors": [],
    "band": 8
 },
 "p": {
    "comment": "The speech is well-paced and easy to understand for the most part. The speaker maintains clear pronunciation and intonation, which helps convey meaning effortlessly. However, some words are pronounced with an accent that may make them difficult to understand for some listeners. ",
    "improvements": "To improve, the speaker could work on their clarity of diction while speaking and focus on the common areas where they tend to struggle with speech. They could also try to listen to and mimic native English speakers' intonation and rhythm.",
    "errors": [],
    "band": 7
 }
}
"""
def estimateTranscription(question,transcription):
    # os.environ["OPENAI_API_KEY"] = API_KEY
    prompt = prompt_template_speaking.format(task=question,response=transcription,format=speaking_format)
    print(prompt)
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user",
             "content": prompt}
        ]
    )
    tmp = completion.choices[0].message["content"]
    print(tmp)
    return tmp