import asyncio

import openai
import os
import json
from langchain.llms import OpenAI
from langchain.memory import ChatMessageHistory
from langchain.memory import ConversationBufferMemory
from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.schema import messages_from_dict, messages_to_dict
import random

from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
import user
StubText = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."
#StubText = "sdfsdfsdf"
SpeakingType = "speaking"
WritingType = "writing"
JsonFormat = '("band","comment")'
Improvements = [
    ["Errors and Grammatics","errors",ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template("You are helpful assistant. Analyze human IELTS writing in English and find errors with grammatical and tenses. Provide list of these errors with rules and explanations, do not do any corrections and not return human writing"),
        HumanMessagePromptTemplate.from_template("\n{answer}")
    ])],
    ["Selfimprovements","selfimprovements",ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template("You are helpful assistant. Analyze human IELTS writing in English and provide list of paraphrasing and changes in sentences to improve writing."),
        HumanMessagePromptTemplate.from_template("\n{answer}")
    ])]
]

IeltsSpeakingTask1CriteriaChat = [
    ["Fluence&Coherence","fc",ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template("You are IELTS Speaking examiner who estimate RESPONSE with scores 1 to 9 by one criteria {input_criteria}. Your response should be only in json format {format} with valid schema. Comment should contain details with at least 150 words"),
        HumanMessagePromptTemplate.from_template("TASK:\n{question}\nRESPONSE:\n{answer}")
    ])],
    ["Lexical Resource","lr",ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template("You are IELTS Speaking examiner who estimate RESPONSE with scores 1 to 9 by one criteria {input_criteria}. Your response should be only in json format {format} with valid schema. Comment should contain details with at least 150 words"),
        HumanMessagePromptTemplate.from_template("RESPONSE:\n{answer}")
    ])],
    ["Grammatical Range and Accuracy", "gra", ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template("You are IELTS Speaking examiner who estimate RESPONSE with scores 1 to 9 by one criteria {input_criteria}. Your response should be only in json format {format} with valid schema. Comment should contain details with at least 150 words"),
        HumanMessagePromptTemplate.from_template("RESPONSE:\n{answer}")
    ])],
    ["Pronunciation", "p", ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template("You are IELTS Speaking examiner who estimate RESPONSE with scores 1 to 9 by one criteria {input_criteria}. Your response should be only in json format {format} with valid schema. Comment should contain details with at least 150 words"),
        HumanMessagePromptTemplate.from_template("RESPONSE:\n{answer}")
    ])],
]

IeltsWritingTask1CriteriaChat = [
    ["Task Achievement","ta",ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template("You are IELTS Writing examiner who estimate RESPONSE with scores 1 to 9 by one criteria {input_criteria}. Your response should be only in json format {format} with valid schema. Comment should contain details with at least 150 words"),
        HumanMessagePromptTemplate.from_template("TASK:\n{question}\nRESPONSE:\n{answer}")
    ])],
    ["Coherence&Cohesion","cc",ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template("You are IELTS Writing examiner who estimate RESPONSE with scores 1 to 9 by one criteria {input_criteria}. Your response should be only in json format {format} with valid schema. Comment should contain details with at least 150 words"),
        HumanMessagePromptTemplate.from_template("RESPONSE:\n{answer}")
    ])],
    ["Grammatical Range and Accuracy", "gra", ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template("You are IELTS Writing examiner who estimate RESPONSE with scores 1 to 9 by one criteria {input_criteria}. Your response should be only in json format {format} with valid schema. Comment should contain details with at least 150 words"),
        HumanMessagePromptTemplate.from_template("RESPONSE:\n{answer}")
    ])],
    ["Lexical Resource", "lr", ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template("You are IELTS Writing examiner who estimate RESPONSE with scores 1 to 9 by one criteria {input_criteria}. Your response should be only in json format {format} with valid schema. Comment should contain details with at least 150 words"),
        HumanMessagePromptTemplate.from_template("RESPONSE:\n{answer}")
    ])],
]


IeltsWritingTask1Criteria = [
    ["Task Achievement","ta",[
        'You are IELTS examiner. Estimate Writing with scores 1 to 9 by {input_criteria}. Reply detailed feedback with examples and improvements in json format (key in lowercase) structure {format}. TASK\n{question} RESPONSE\n{answer}'
    ]],
    ["Coherence and Cohesion", "cc",[
        'You are IELTS examiner. Estimate Writing with scores 1 to 9 by {input_criteria}. Reply detailed feedback with examples and improvements in json format (key in lowercase) structure {format}. {answer}'
    ]],
    ["Lexical Resource", "lr",[
        'You are IELTS examiner. Estimate Writing with scores 1 to 9 by {input_criteria}. Reply detailed feedback with examples and improvements in json format (key in lowercase) structure {format}. {answer}'
    ]],
    ["Grammatical Range and Accuracy","gra",[
        'You are IELTS examiner. Estimate Writing with scores 1 to 9 by {input_criteria}. Reply detailed feedback with examples and improvements in json format (key in lowercase) structure {format}. {answer}'
    ]]
]

IeltsSpeakingTask1Criteria = [
    ["Fluence&Coherence","fc",[
        'You are IELTS Speaking examiner why estimate RESPONSE with scores 1 to 9 by one criteria {input_criteria}. who can only answer in json format. Reply detailed feedback with examples and improvements in json format (key in lowercase) structure {format}. TASK is the question. RESPONSE is human answer. TASK\n{question} \nRESPONSE\n{answer}.'
    ]],
    ["Lexical Resource", "lr",[
        'You are IELTS Speaking examiner. TASK is the question. Estimate only RESPONSE with scores 1 to 9 by {input_criteria}. Reply detailed feedback with examples and improvements in json format (key in lowercase) structure {format}. RESPONSE\n{answer}'
    ]],
    ["Grammatical Range and Accuracy","gra",[
        'You are IELTS Speaking examiner. TASK is the question. Estimate only RESPONSE with scores 1 to 9 by {input_criteria}. Reply detailed feedback with examples and improvements in json format (key in lowercase) structure {format}. RESPONSE\n{answer}'
    ]],
    ["Pronunciation","p",[
        'You are IELTS Speaking examiner. TASK is the question. Estimate only RESPONSE with scores 1 to 9 by {input_criteria}. Reply detailed feedback with examples and improvements in json format {format}. RESPONSE\n{answer}'
    ]]

]
GlobalNumberOfCriteria = len(IeltsWritingTask1Criteria)
def GenerateConfigForUser(inputuser,model):
    level =  user.getUserLevel(inputuser)
    if (model =="completition"):
        model_name = "text-davinci-003"
    else:
        model_name = "gpt-3.5-turbo"
    temperature = 1.0
    random_criterias = list(range(0,GlobalNumberOfCriteria))
    chat_criterias = []
    improvements = False;
    if (level == 0):
        max_tokens=300
        # rnd = random.randint(0,GlobalNumberOfCriteria-1)
        # random_criterias.remove(rnd)
        # chat_criterias = [rnd]
    elif (level==1):
        max_tokens=300
        chat_criterias = random_criterias
        random_criterias = []
    else:
        max_tokens = 300
        chat_criterias = random_criterias
        random_criterias = []
        improvements = True

    resp = {
        'level': level,
        'model_name': model_name,
        'temperature': temperature,
        'max_tokens': max_tokens,
        'random_criterias': random_criterias,
        'chat_criterias': chat_criterias,
        'improvements': improvements
    }
    print(inputuser)
    print(resp)
    return resp










openai.api_key = os.environ["OPENAI_API_KEY"]

def memory():

    history = ChatMessageHistory()
    history.ad
    history.add_user_message("hi!")
    memory = ConversationBufferMemory()

    llm = OpenAI(temperature=0)
    conversation = ConversationChain(
        llm=llm,
        verbose=True,
        memory=memory
    )
    conversation.predict(input="Hi there, my name is Alex");
    conversation.predict(input="what is my name?")
    conversation.predict(input="bue!")
    dicts = messages_to_dict(conversation)
    print(dicts)
def voiceToText(filename):
    if True:
        audio_file = open(filename, "rb")
        # resp = openai.Audio.transcribe("whisper-1", audio_file)
        resp = openai.Audio.translate("whisper-1", audio_file)
        print(resp)
        tmp = resp['text']
        print(tmp)
        return tmp

async def async_generate_random_improvement(key):
    tmp = {"comment": StubText, "stub":True}
    print(tmp)
    return [key,tmp]
async def async_generate_random_criteria(key):
    tmp = {"band": str(random.randint(1,9)), "comment": StubText, "stub": True}
    print(tmp)
    return [key,tmp]

async def async_generate_criteria(llm, msg, key):
    print(msg)
    resp = await llm.agenerate(msg)
    rsp = resp.generations[0][0].text
    print(rsp)
    tmp = json.loads(resp.generations[0][0].text,strict=False)
    tmp['stub'] = False
    print(tmp)

    return [key,tmp]


async def async_generate_improvement(llm, msg, key):
    resp = await llm.agenerate(msg)
    tmp = resp.generations[0][0].text

    resp = {"comment":tmp, "stub": False}
    return [key,resp]
# async def conversation_async(question,answer):
#     model_name = "gpt-3.5-turbo"
#     chat = ChatOpenAI(model_name=model_name)
#     template_criteria = 'Say hello to {name}'
#     human_template = "{answer}"
#     system_message_prompt = SystemMessagePromptTemplate.from_template(template_criteria)
#     human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
#     chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
#     IeltsWritingTask1Criteria = [
#         "Alex",
#         "Anna",
#         "Johnny"
#     ]
#     res = [];
#     for i in range(len(IeltsWritingTask1Criteria)):
#         tmp_msg = chat_prompt.format_prompt(name=IeltsWritingTask1Criteria[i],answer="hi").to_messages()
#         res.append(async_generate(chat,[tmp_msg]))
#     done = await asyncio.gather(*res)
#
#     for future in done:
#         print(future)
#     resp = {
#         'test': "response"
#     }
#     return resp

async def WritingEstimationCompletition(question, answer,user,type):
    config = GenerateConfigForUser(user,"completition")
    llm = OpenAI(model_name=config['model_name'], max_tokens=config['max_tokens'],temperature=config['temperature'])
    if (type==WritingType):
        prompt = IeltsWritingTask1Criteria
    else:
        prompt = IeltsSpeakingTask1Criteria
    criterias = []
    for i in config['chat_criterias']:
        msg = prompt[i][2][0].format(input_criteria=prompt[i][0],answer=answer,question=question,format=JsonFormat)
        criterias.append(async_generate_criteria(llm, [msg], prompt[i][1]))
    for j in config['random_criterias']:
        criterias.append(async_generate_random_criteria(prompt[j][1]))

    if config["improvements"] == False:
        for k in range(len(Improvements)):
            criterias.append(async_generate_random_improvement(Improvements[k][1]))
    else:
        for k in range(len(Improvements)):
            msg = Improvements[k][2][0].format(answer=answer)
            criterias.append(async_generate_improvement(llm,[msg],Improvements[k][1]))



    done = await asyncio.gather(*criterias)
    response = {}
    for value in done:
        print(value)
    for value in done:
        print(value[1])
        response[value[0]] = value[1]
    response['level']=config['level']
    response['improvements'] = config['improvements']
    print(response)
    return response


async def WritingEstimationChat(question, answer,user,type):
    config = GenerateConfigForUser(user,"chat")
    llm = ChatOpenAI(model_name=config['model_name'], max_tokens=config['max_tokens'], temperature=config['temperature'])
    if (type == WritingType):
        prompt = IeltsWritingTask1CriteriaChat
    else:
        prompt = IeltsSpeakingTask1CriteriaChat
    criterias = []
    for i in config['chat_criterias']:
        msg = prompt[i][2].format_prompt(input_criteria=prompt[i][0], answer=answer, question=question, format=JsonFormat).to_messages()
        criterias.append(async_generate_criteria(llm, [msg], prompt[i][1]))
        #criterias.append(async_generate_random_criteria(prompt[i][1]))
    for j in config['random_criterias']:
        criterias.append(async_generate_random_criteria(prompt[j][1]))

    if config["improvements"] == False:
        for k in range(len(Improvements)):
            criterias.append(async_generate_random_improvement(Improvements[k][1]))
    else:
        for k in range(len(Improvements)):
            msg = Improvements[k][2].format_prompt(input_criteria=Improvements[k][0], answer=answer).to_messages()
            criterias.append(async_generate_improvement(llm, [msg], Improvements[k][1]))

    done = await asyncio.gather(*criterias)
    response = {}
    for value in done:
        print(value[1])
        response[value[0]] = value[1]
    response['level'] = config['level']
    response['improvements'] = config['improvements']
    print(response)
    return response

