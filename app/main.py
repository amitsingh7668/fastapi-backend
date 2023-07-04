from fastapi import FastAPI, HTTPException,File, UploadFile
from starlette.responses import Response
import requests
import json
import os
import openai
import json
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    team_members=[{1:"Santosh"},{2:"Datta"},{3:"Deeksha"},{4:"Amit"}]
    return {"Presenting": "GH hackathon",
    "Team":"Developers",
    "About":"Extract TRF data from pdf and return json , and also have capability of prompt engineering",
    "Github Repository": "https://xyz.com",
    "Team_members":team_members}


@app.post("/uploadfile/")
def create_upload_file(file: UploadFile,question:str):
    answer=""
    split_question = question.split(",")
    data=[]
    for spl in split_question:
        print(spl)
        for key in data_lazarus():
            if spl.lower() in key.lower(): 
                data.append({'question':key,'answer':data_lazarus()[key]})

    print(data)
    return {"filename": file.filename,'data':data}

@app.post("/uploadfile/openai")
def create_upload_file(file: UploadFile,question:str):
    answer=""
    split_question = question.split(",")

    openai_data = extract_data_lazarus(file,question)
    data=[]
    data.append({'question':question,'answer':openai_data})

    return {"filename": file.filename,'data':data}

@app.get("/api/data")
def dict_data():
    return data_lazarus()

def data_lazarus(filenameval):
    f = open("data/"+filenameval)
    data = json.load(f)
    return data

def extract_data_lazarus(file_data,question_main):
    #return "uncomment code"
    url = "https://api.lazarusforms.com/api/forms/generic"
    print("Starts reading file from lazarus api ,,,,")
    payload={}
    openai.api_key = "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"
    files=[('file',('file_name',file_data.file,'application/octet-stream'))]
    headers = {
    'orgId': 'cd6a73a119c44419ad',
    'authKey': '6a7e5072c92a4140af28',
    'version': '2'
    }
    
    flag = True
    filenameInDict = ""
    for x in os.listdir("./data"):
            if str(file_data.filename) in x:
                print(file_data.filename)
                filenameInDict= x
                flag=False
  
    if flag:
        response = requests.post(url, headers=headers, data=payload, files=files)

        print(" Json recieved from lazarus")
        # json_object = json.dumps(response.json(), indent=4)
        dict_temp = {}

        for a in response.json()['keyValuePairs']:
            try:
                dict_temp[a['key']['content']] = a['value']['content']
            except:
                pass
        json_object = json.dumps(dict_temp, indent = 4)
        # print(json_object)

        with open("data/"+file_data.filename+".json", "w") as outfile:
            outfile.write(json_object)
    else:
        print("Data is available in cache ...")
        json_object = data_lazarus(filenameInDict)
        
    question_suffix = "In the above string "    
    
    actual_question = str(json_object) + " "+str(question_suffix)+" "+str(question_main)
    
    print(actual_question)

    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content":actual_question}
    ])
    print(completion.choices[0].message["content"])

    return completion.choices[0].message["content"]
