# scratch work doc

import re
import os
import json
import spacy
#import fasttext
import urllib.request
from bs4 import BeautifulSoup
#from deepsegment import DeepSegment
import nltk
from nltk.corpus import stopwords


VALID_CHARS = set("abcdefghijklmnopqrstuvwxyz123456789. ")


"""
model = fasttext.load_model(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "model_1000000.ftz")
)

segmenter = DeepSegment("en")

"""

class IMP:
    def __init__(self, sentence):
        nlp = spacy.load("en_core_web_md")
        
        merge_ncs = nlp.create_pipe("merge_noun_chunks")
        merge_ents = nlp.create_pipe("merge_entities")
        nlp.add_pipe(merge_ents)
        nlp.add_pipe(merge_ncs) 


        self.doc= nlp(sentence)

    def preprocess_text(self, text):
    
        return "".join(c for c in text.lower() if c in VALID_CHARS)

    def get_noun_chunks(self):
        chunks=[]
        stop_words= set(stopwords.words('english'))
        for chunk in self.doc.noun_chunks:
            chunks.append(chunk.text)
        str= " ".join(chunks)
        str= str.split()
        filtered_sentence= [w for w in str if w not in stop_words]
        return " ".join(filtered_sentence)

    def get_pos(self):
        out={}
        for text in self.doc:
            if text.dep_ == "nsubj":
                out["subject"] = text.orth_
            if text.dep_ == "iobj":
                out["indirect_object"] = text.orth_
            if text.dep_ == "dobj":
                out["direct_object"] = text.orth_
        
        return (out)
        

    def get_title(self, OPTIMAL_LENGTH=3):
        def _from_verb(verb):
            phrase = []
            current = []
            for child in verb.children:
                if child.pos_ in ("NOUN", "VERB", "CCONJ", "ADP") and child.dep_ in (
                    "cc",
                    "pobj",
                    "dobj",
                    "conj",
                    "xcomp",
                    "pcomp",
                    "advcl",
                ):
                    current.extend(child.subtree)
                if child.pos_ in ("NOUN", "VERB"):
                    phrase.extend(current)
                    current = []
            return phrase if phrase else list(verb.subtree)

        candidate = None
        for verb in filter(lambda x: x.pos_ in ("VERB", "ADP"), self.doc):
            phrase = _from_verb(verb)
            if (
                phrase
                and any(
                    token.pos_ in "NOUN" or token.dep_.endswith("comp") for token in phrase
                )
                and (
                    not candidate
                    or (
                        abs(len(phrase) - OPTIMAL_LENGTH)
                        < abs(len(candidate) - OPTIMAL_LENGTH)
                        and phrase
                    )
                )
            ):
                candidate = phrase

        if candidate is None:
            return rawtext
 
        return " ".join(map(str, candidate))


model= IMP("Calculate the friction on the ball as its rolling down the hill")

#print(model.get_title())

#test1= "How much work is done by the man to lift a 3kg object 2 meters"
#print (model.get_pos())

print(model.get_noun_chunks())


