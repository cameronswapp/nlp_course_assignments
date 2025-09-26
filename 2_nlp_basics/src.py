"""
WEEK 2

- Assumes you've pip installed requirements file (pip install -r requirements.txt)
- Also need to download English trained pipeline https://spacy.io/models/en#en_core_web_sm. This can be done using
    `python -m spacy download en_core_web_sm` which downloads the model as another pip package essentially.
"""
from PyPDF2 import PdfReader
import spacy
from spacy import displacy

# Assumes this model is already downloaded
nlp = spacy.load("en_core_web_sm")


def pdf_entity_extractor(pdf_file_location, display_file_location: str = None) -> dict[str, list[str]]:
    """
    Return a dictionary of entities from a pdf. Optionally display entities via displacy.
    :param pdf_file_location: file location of the pdf to analyze.
    :param display_file_location: whether to display sentence with entities
    :return: dictionary of entities. Should be formmated like so:
        {
            "entity_label": ["list", "of", "entities"],
            ...
        }

        For example,

        {
            "ORG": ["USU", "BYU"],
            ...
        }

    """
    file = PdfReader(pdf_file_location)
    text = ""
    for page in file.pages:
        text += page.extract_text()

    doc = nlp(text)
    
    dictionary = {}
    for entity in doc.ents:
        if entity.label_ not in dictionary:
            dictionary[entity.label_] = [entity.text]
        else:
                dictionary[entity.label_].append(entity.text)

    if display_file_location:
        html = displacy.render(doc, style="ent", page=True, jupyter=False)
        with open(display_file_location, "w", encoding="utf-8") as f:
            f.write(html)

    return dictionary


def token_analyzer(text: str, display_file_location: str = None) -> dict:
    """
    Given a text string, split into tokens and return for each token:
        - the lemmatized version of each token,
        - the part of speech,
        - the shape,
        - whether alpha characters are present in the token
        - whether the token is a stop word

    :param text: sentence string to analyze.
    :param display_file_location: whether to display dependencies and pos
    :return: dictionary of tokens, formatted like this:
        {
            'token A': {
                'lemma': 'token A lemma',
                'pos': 'token A pos',
                'shape': 'token A shape',
                ...
            },
            'token B': {
                ...
            }
        }
    """
    dictionary = {}
    doc = nlp(text)
    for token in doc:
        dictionary[token.text] ={'lemma': token.lemma_, 'pos': token.pos_, 'shape': token.shape_, 'isAlpha': token.is_alpha, 'isStopWord': token.is_stop}

    if display_file_location:
        html = displacy.render(doc, style="dep", page=True, jupyter=False)
        with open(display_file_location, "w", encoding="utf-8") as f:
            f.write(html)

    return dictionary



def remove_stop_words(text: str) -> str:
    """
    Remove stop words: https://spacy.io/usage/linguistic-features#language-data
    :param text: original sentence, text
    :return: same string, but without stop words
    """
    finalString = ""
    doc = nlp(text)
    for token in doc:
        if not token.is_stop:
            finalString += token.text + " "

    return finalString



def lemmatizer(text: str) -> str:
    """
    Lemmatize sentence.
    :param text: original sentence, text to lemmatize
    :return: lemmatized text
    """
    finalString = ""
    doc = nlp(text)
    for token in doc:
        finalString += token.lemma_ + " "

    return finalString



def create_character_tokenizer(training_text: str, text_to_tokenize: str) -> list[int]:
    """
    Given a training text corpus and the text to tokenize, first find a character level tokenization from the training
    text apply to the text to tokenize.

    For example:
    create_character_tokenizer('abcd', 'acb') -> [0,2,1]

    :param training_text: larger corpus of text to find a character level tokenization from.
    :param text_to_tokenize: text to tokenize using found character level tokenization.
    :return: list of the tokens.
    """
    tokens = {}
    for i in range(len(training_text)):
        if training_text[i] not in tokens:
            tokens[training_text[i]] = i

    tokenList = []
    for i in range(len(text_to_tokenize)):
        if text_to_tokenize[i] in tokens:
            tokenList.append(tokens[text_to_tokenize[i]])
    
    return tokenList
