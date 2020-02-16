import time
import logging
from flask import Flask, Response, request, jsonify
import requests
import werkzeug
import json

AZURE_OCR = "https://westus.api.cognitive.microsoft.com/vision/v2.0/ocr?language=en"
AZURE_TEXT_ANALYTICS = "https://treehacks-text.cognitiveservices.azure.com/text/analytics/v2.1/keyPhrases"
AZURE_BING = "https://treehacks-bing-image-search.cognitiveservices.azure.com/bingcustomsearch/v7.0/images/search?q=%s&customconfig=d0095db6-9d62-4760-96bd-c07dce1bdb1c"

app = Flask(__name__)

@app.route('/api', methods=['POST'])
def handle_request():
    imagefile = request.files['image']

    # azure ocr
    headers = {'Ocp-Apim-Subscription-Key': 'KEY1',
               'Content-Type': 'application/octet-stream', }
    r = requests.post(AZURE_OCR, headers=headers, data=imagefile)

    json_response = r.json()

    textDeg = json_response['textAngle']
    lines = [{"textAngle": textDeg}]
    allText = []

    for idx, det in enumerate(json_response['regions']):
        lineStr = ""

        for line in det['lines']:
            lineStr = " ".join([word['text'] for word in line['words']])

        bounding = [int(x) for x in det['boundingBox'].split(",")]
        lineObj = {"x": bounding[0],
                   "y": bounding[1],
                   "w": bounding[2],
                   "h": bounding[3],
                   "line": lineStr}
        lines.append(lineObj)

        allText.append({"language": "en",
                        "id": idx,
                        "text": lineStr})

    # get keywords
    headers = {'Ocp-Apim-Subscription-Key': 'KEY2'}
    payload = {"documents": allText}
    r = requests.post(AZURE_TEXT_ANALYTICS, headers=headers, json=payload)
    text_preds = r.json()

    allSimplified = []
    for doc in text_preds['documents']:
        allSimplified.append(" ".join(doc['keyPhrases']))

    imgurls = []
    headers = {'Ocp-Apim-Subscription-Key': 'KEY3'}

    for sentence in allSimplified:
        if (sentence.replace(" ", "+") != ''):
            # get images
            r = requests.get(AZURE_BING % sentence.replace(" ", "+"), headers=headers)
            ret_docs = r.json()

            if (len(ret_docs['value']) >= 1):
                imgurls.append(ret_docs['value'][0]['contentUrl'])

    # return ocr result + image urls
    return jsonify({'ocr': lines}, {'image-urls': imgurls}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
