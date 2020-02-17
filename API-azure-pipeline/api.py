import time
import logging
from flask import Flask, Response, request, jsonify
import requests
import werkzeug
import json
import spacy
import random

AZURE_OCR = "https://westus.api.cognitive.microsoft.com/vision/v2.0/ocr?language=en"
AZURE_TEXT_ANALYTICS = "https://treehacks-text.cognitiveservices.azure.com/text/analytics/v2.1/keyPhrases"
AZURE_BING = "https://treehacks-bing-image-search.cognitiveservices.azure.com/bingcustomsearch/v7.0/images/search?q=%s&customconfig=d0095db6-9d62-4760-96bd-c07dce1bdb1c"

app = Flask(__name__)

@app.route('/api', methods=['POST'])
def handle_request():
    imagefile = request.files['image']

    # azure ocr
    headers = {'Ocp-Apim-Subscription-Key': 'cf58dd90966a443eb07bf720bef831ed',
               'Content-Type': 'application/octet-stream', }
    r = requests.post(AZURE_OCR, headers=headers, data=imagefile)

    json_response = r.json()

    lines = []
    allText = []

    print(json_response['regions'])

    for idx, det in enumerate(json_response['regions']):
        lineStr = ""
        tmpLine = ""

        for line in det['lines']:
            tmpLine = " ".join([word['text'] for word in line['words']]) + " "
            lineStr += tmpLine


        bounding = [int(x) for x in det['boundingBox'].split(",")]
        lineObj = {"x": bounding[0],
                   "y": bounding[1],
                   "w": bounding[2],
                   "h": bounding[3],
                   "line": lineStr}
        lines.append(lineObj)

        allText.append({"language": "en",
                        "id": idx,
                        "text": tmpLine})

    # get keywords
    headers = {'Ocp-Apim-Subscription-Key': 'e499e8daa7ea4f609e0dc5772771cea8'}
    payload = {"documents": allText}
    r = requests.post(AZURE_TEXT_ANALYTICS, headers=headers, json=payload)
    text_preds = r.json()

    if 'documents' in text_preds:
        allSimplified = []
        for doc in text_preds['documents']:
            allSimplified.append(" ".join(doc['keyPhrases']))
    else:
        return jsonify({'ocr': [], 'image-urls': []}), 200

    imgurls = []
    headers = {'Ocp-Apim-Subscription-Key': '7bfd359d42614c3888bbb25998062080'}

    for sentence in allSimplified:
        if (sentence.replace(" ", "+") != ''):
            # get images
            r = requests.get(AZURE_BING % sentence.replace(" ", "+"), headers=headers)
            ret_docs = r.json()

            if (len(ret_docs['value']) >= 1):
                imgurls.append(ret_docs['value'][0]['contentUrl'])

    # return ocr result + image urls
    print(lines)
    return jsonify({'ocr': lines, 'imageUrls': imgurls}), 200

@app.route('/rnd_wsd', methods=['POST'])
def handle_rnd():
    input_text = request.args["q"]
    chunk = random.choice(q.get_chunks(input_text))



    return jsonify({'output': finished_quiz}), 200

@app.route('/quiz', methods=['POST'])
def handle_quiz():
    input_text = request.args["q"]
    finished_quiz=q.get_quiz(input_text)

    return jsonify({'output': finished_quiz}), 200


#  --- Quiz Stuff ---
class Quiz:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_md")
        
        merge_ncs = self.nlp.create_pipe("merge_noun_chunks")
        merge_ents = self.nlp.create_pipe("merge_entities")
        self.nlp.add_pipe(merge_ents)
        self.nlp.add_pipe(merge_ncs) 

    def get_chunks(self, text):
        nouns=[]
        list_of_sentences= text.split(".")
        for sentence in list_of_sentences:
            parsed_sentence = self.nlp(sentence)
            li_parsed_sentence= list(parsed_sentence)
            nouns.extend(list(parsed_sentence.noun_chunks))
        return nouns
    
    def get_quiz(self, text):
        quiz=[]
        list_of_sentences= text.split(".")
        for sentence in list_of_sentences:
            qa_dic={}
            parsed_sentence = self.nlp(sentence)
            li_parsed_sentence= list(parsed_sentence)
            #print(li_parsed_sentence)
            chunks = list( parsed_sentence.noun_chunks )
    
            if len(chunks)>2:
                first_chunk= chunks[1]
                answer= first_chunk.text
                qa_dic["answer"]= first_chunk.text
                li_text= [i.text for i in li_parsed_sentence]
                #qa_dic["distractors"]= self.generate_distractors(answer)
                index_of_first_chunk= li_text.index(answer)
                li_text[index_of_first_chunk]= "_____"
                qa_dic["question"]= " ".join(li_text)
                quiz.append(qa_dic)
        return quiz

if __name__ == '__main__':
    q = Quiz()
    app.run(host="0.0.0.0", port=8080)
