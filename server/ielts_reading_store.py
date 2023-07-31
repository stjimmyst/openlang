from olfirestore import OL_firestore
import json
import uuid
import gpt
import asyncio


async def initLoad():
    file_path = "../test/ielts-reading.json"
    f = open(file_path)
    init_data = json.load(f)
    explanations_task = []
    for init_section in init_data['sections']:
        for content in init_section['contents']:
            explanations_task.append(gpt.IeltsReadingQuestionsExplanation(content))
    done = await asyncio.gather(*explanations_task)
    explanations = {}

    for section in done:
        for question in section:
            explanations[question['question_id']] = question['explanation']

    print("explanations done")
    print(json.dumps(explanations))


    tmp = init_data
    reading_exam_id = str(uuid.uuid4())
    tmp['exam_id'] = reading_exam_id
    tmp_sections = []
    tmp_plain_questions=[]
    for init_section in init_data['sections']:
        tmp_section = {}

        tmp_section_uuid = str(uuid.uuid4())
        tmp_section['section_id'] = tmp_section_uuid
        tmp_section['section_number'] = init_section['section_number']
        tmp_contents = []
        min_question = 999
        max_question = -1
        for init_content in init_section['contents']:
            tmp_content = init_content
            tmp_questions = []
            for init_question in init_content['questions']:

                tmp_question = init_question
                tmp_items=[]
                for init_item in init_question['items']:
                    tmp_item_uuid = str(uuid.uuid4())
                    tmp_item = init_item
                    tmp_item['item_uuid'] = tmp_item_uuid
                    item_text = str(init_item['item_text']).replace("__question", "__" + tmp_item_uuid)
                    tmp_item['item_text'] = item_text
                    tmp_item['item_explanation'] = explanations[init_item['item_number']]
                    tmp_question['items'] = tmp_item
                    tmp_items.append(tmp_item)
                    tmp_plain_questions.append(tmp_item)
                    if (init_item['item_number'] <min_question):
                        min_question = init_item['item_number']
                    if (init_item['item_number'] > max_question):
                        max_question = init_item['item_number']
                tmp_question['items']=tmp_items
                tmp_questions.append(tmp_question)
            tmp_content['content_id']=str(uuid.uuid4())
            tmp_content['content_id'] = str(uuid.uuid4())
            tmp_content['questions']=tmp_questions

            tmp_contents.append(tmp_content)
        tmp_section['section_description'] = "Questions " + str(min_question) + "-" + str(max_question)
        tmp_section['contents'] = tmp_contents

        tmp_sections.append(tmp_section)
    tmp['sections'] = tmp_sections
    tmp['plain-answers'] = tmp_plain_questions

    print(json.dumps(tmp))
    OL_firestore.collection("ielts_reading").add(init_data, reading_exam_id)

asyncio.run(initLoad())

