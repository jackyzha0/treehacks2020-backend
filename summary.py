import re
import os
import json
import spacy


class Summary:
    def __init__(self, rawtext):
        self._summary = self._generate_summary(rawtext)

    def _generate_summary(self, rawtext):
        nlp = spacy.load("en_core_web_md")
        doc = nlp(rawtext)

        roots = sorted(
            filter(lambda t: t.pos_ == "VERB", doc), key=lambda t: len(list(t.children))
        )
        already_covered = frozenset()

        def build_phrase(root):
            phrase = []
            processed_verbs = frozenset([root])
            added = False
            for child in root.children:
                if child in already_covered:
                    return -1, -1
                if child.i > root.i and not added:
                    phrase.append(root)
                    added = True
                if child.pos_ in ("VERB", "ADP"):
                    phrase_segment, new_processed_verbs = build_phrase(child)
                    if phrase_segment == -1:
                        return -1, -1
                    phrase.extend(phrase_segment)
                    processed_verbs |= new_processed_verbs
                elif child.pos_ not in ("PART", "INTJ", "DET") and (
                    child.pos_ != "ADV" or child.text in ("never", "not", "nt")
                ):
                    phrase.append(child)
                    if child.pos_ in ("NUM", "ADJ"):
                        for of in filter(lambda g: str(g) == "of", child.children):
                            phrase_segment, new_processed_verbs = build_phrase(of)
                            if phrase_segment == -1:
                                return -1, -1
                            phrase.extend(phrase_segment)
                            processed_verbs |= new_processed_verbs
            if not added:
                phrase.append(root)
            if len(phrase) <= 1:
                phrase = []
            return phrase, processed_verbs

        phrases = []
        while roots:
            root = roots.pop()
            phrase, processed_verbs = build_phrase(root)
            if phrase != -1:
                if phrase:
                    phrases.append(phrase)
                already_covered |= processed_verbs
                roots = list(filter(lambda t: t not in processed_verbs, roots))

        phrases.sort(key=lambda t: t[0].i)
        unsanitized = [" ".join(map(str, xs)) for xs in phrases]
        kindasanitized = [
            "".join(
                c for c in bullet.lower() if c.isdigit() or c.isalpha() or c.isspace()
            )
            for bullet in unsanitized
        ]
        mostlysanitized = [
            " ".join(c for c in bullet.split(" ") if c) for bullet in kindasanitized
        ]
        almostcompletelysanitized = [x for x in mostlysanitized if x.count(" ") <= 10]
        return [b.capitalize() for b in almostcompletelysanitized]

    def json(self):
        return {"genre": "summary", "content": self._summary}



text="Consider a force like gravitation which varies predominantly inversely as the square of the distance, but which is about a billion-billion-billion-billion times stronger. And with another difference. There are two kinds of matter, which we can call positive and negative. Like kinds repel and unlike kinds attract—unlike gravity where there is only attraction. What would happen?"

S= Summary(text)

text2= "There is such a force: the electrical force. And all matter is a mixture of positive protons and negative electrons which are attracting and repelling with this great force. So perfect is the balance, however, that when you stand near someone else you don’t feel any force at all. If there were even a little bit of unbalance you would know it. If you were standing at arm’s length from someone and each of you had one percent more electrons than protons, the repelling force would be incredible. How great? Enough to lift the Empire State Building? No! To lift Mount Everest? No! The repulsion would be enough to lift a “weight” equal to that of the entire earth!"
print( S._summary )