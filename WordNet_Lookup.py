from nltk.corpus import wordnet as wn

def WN_lookup(wn30_key):
    lemma = wn.lemma_from_key(wn30_key)
    synset = lemma.synset()
    return synset.definition()