import spacy
from nltk.corpus import stopwords
import logging

class NounChunk:
    def __init__(self):
        logging.info("Loading NounChunker deps")
        self.nlp = spacy.load("en_core_web_md")
        
        merge_ncs = self.nlp.create_pipe("merge_noun_chunks")
        merge_ents = self.nlp.create_pipe("merge_entities")
        self.nlp.add_pipe(merge_ents)
        self.nlp.add_pipe(merge_ncs) 

    def get_noun_chunks(self, sentence):
        parsed_sentence = self.nlp(sentence)
        chunks=[]
        stop_words= set(stopwords.words('english'))
        for chunk in parsed_sentence.noun_chunks:
            chunks.append(chunk.text)
        str= " ".join(chunks)
        str= str.split()
        filtered_sentence= [w for w in str if w not in stop_words]
        return " ".join(filtered_sentence)