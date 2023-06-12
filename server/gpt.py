import openai
import json

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

def estimate_text(question, answer):
    openai.api_key = API_KEY
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
    return tmp