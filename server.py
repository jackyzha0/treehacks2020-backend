import logging
import flask
from flask import jsonify
from flask import request

from BERT_pred import BERT_pred

app = flask.Flask(__name__)


@app.route('/', methods=['GET'])
def healthCheck():
    logging.info("Health check ping received")
    return jsonify({'status': 'healthy'}), 200


@app.route('/api', methods=['POST'])
def parseIntent():
    data = flask.request.form  # is a dictionary
    sentence = data['sentence']
    word = data['word']
    answer = m.predict(sentence, word)

    logging.info("word: " + answer[0])
    return jsonify({'def': answer[0]}), 200

if __name__ == '__main__':
    logging.info("Starting server...")
    m = BERT_pred("BERT_semcor.pickle")
    app.run(host="0.0.0.0", port=5000)
