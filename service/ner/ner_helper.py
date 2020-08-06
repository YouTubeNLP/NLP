import spacy
from nerd import ner

# function to apply ner using spacy library
def spacy_ner(document):
    nlp = spacy.load("en_core_web_sm") 
    doc = nlp(document)
    results = [(ent.text, ent.label_) for ent in doc.ents]
    return results


# function to apply ner using nerd library
def nerd_ner(document):
    doc = ner.name(document, language='en_core_web_sm')
    results = [(ent.text, ent.label_) for ent in doc]
    return results