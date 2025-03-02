import base64
import requests
import json

 


class INK:
    def __init__(self, s: str):
        self.s = s

    def scrab(self, data):
        s = data
        b = {}


        url = "http://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.s}"
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            b = response.json()
        else:
            b = {"error": f"Request failed with status code {response.status_code} with proxy hub"}

        return b

    def summarize(self, data):
        s = data
        b = {}

        ptp = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a expert content summarizer. Your task is to simplify the given content so that a student can understand it easily."
                },
                {
                    "role": "user",
                    "content": f"Query: {s['prompt']}"
                },
                {
                    "role": "user",
                    "content": f"Content: {s['content']}"
                }
            ],
            "temperature": 0.7,
            "response_format": {
                "type": "json_schema",
                "json_schema": {
                "name": "sumup",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "summary": {"type": "string"}
                    },
                    "required": ["summary"],
                    "additionalProperties": False,
                },
            },
            }
        }

        b = json.loads(self.scrab(ptp)['choices'][0]['message']['content'])
        
        return b

    def generate_questions(self, data):
        s = data
        b = {}

        ptp = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                "role": "system",
                "content": "You are a question generation assistant. Your task is to produce exactly N questions based on the topic and detailed scope provided by the user. Each question must be concise and stay within the subject boundaries defined. Do not output any extra text—only a JSON object as specified in the schema."
                },
                {
                    "role": "user",
                    "content": f"Query: {s['prompt']}"
                },
                {
                    "role": "user",
                    "content": f"Content: {s['content']}"
                }
            ],
            "temperature": 0.7,
            "response_format": {
                "type": "json_schema",
                "json_schema": {
                "name": "MCQSchema",
                "schema": {
                    "type": "object",
                    "properties": {
                        "questions": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "question": {"type": "string"},
                                    "options": {
                                        "type": "object",
                                        "properties" : {
                                            "A" : {"type": "string"},
                                            "B" : {"type": "string"},
                                            "C" : {"type": "string"},
                                            "D" : {"type": "string"},
                                        },
                                        "required": ["A", "B", "C", "D"], 
                                    },
                                    "answer": {"type": "string"}
                                },
                                "required": ["question", "options", "answer"]
                            },
                        }
                    },
                    "required": ["questions"]
                    
                }
                }
            }
        }

        dat = json.loads(self.scrab(ptp)['choices'][0]['message']['content'])
        ques = dat['questions']

        for question_data in ques:
            print(f"Question: {question_data['question']}\n")
            
            for option, answer in question_data['options'].items():
                if option == question_data['answer']:
                    print(f"\033[32m{option}. {answer}\033[0m")  # Correct answer in green
                else:
                    print(f"{option}. {answer}")  # Other options in default color
            
            print()

        b = ques
        return b

    def chat(self, data):
        s = data
        b = {}

        qo = [ "Asking Solution", "normal chat", "motivation", "Asking direct answer" ]

        ptp = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "system",
                    "content": f"You are the advance level query classifier from the options {qo}. You output the index, its label, and tell what the user is trying to do from this array for the type of query the user is asking"
                },
                {
                    "role": "user",
                    "content": f"Query: {s['prompt']}"
                }
            ],
            "temperature": 0.3,
            "response_format": {
                "type": "json_schema",
                "json_schema": {
                "name": "summarize",
                    "schema": {
                        "$schema": "http://json-schema.org/draft-04/schema#",
                        "title": "Model",
                        "type": "object",
                        "properties": {
                            "index": {"type": "number"},
                            "label": {"type": "string"},
                            "response" : {"type": "string"}
                        }
                    }
                }
            }
        }
        

        dat = json.loads(self.scrab(ptp)['choices'][0]['message']['content'])
        b = dat
        
        return b

    def surprise_features(self, data):
        b = {}
        return b

ink = INK("eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIyZjMwMDA2MDVAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.3Obdi1LKmdOki-kPPdF_QtPlcNA-5opr6Txsv5Vccho")

# ink.generate_questions({
#     "topic" : "Data Types 1",  #"https://www.youtube.com/watch?v=8n4MBjuDBu4"
#     "scope" : "Consider it yourself accoding to topic",
#     "N" : 5
# })