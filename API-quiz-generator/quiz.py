from flask import Flask, Response, request, jsonify
import json
import spacy

app = Flask(__name__)

class Quiz:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_md")
        
        merge_ncs = self.nlp.create_pipe("merge_noun_chunks")
        merge_ents = self.nlp.create_pipe("merge_entities")
        self.nlp.add_pipe(merge_ents)
        self.nlp.add_pipe(merge_ncs) 
    
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

@app.route('/quiz', methods=['POST'])
def handle_request():
    input_text = request.args["q"]
    finished_quiz=q.get_quiz(input_text)

    return jsonify({'output': finished_quiz}), 200

if __name__ == '__main__':
    q = Quiz()
    app.run(host="0.0.0.0", port=8081)
