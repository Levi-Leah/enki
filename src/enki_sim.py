import spacy

nlp = spacy.load("en_core_web_lg")

w1 = 'red'
w2 = 'run'

w1 = nlp.vocab[w1]
w2 = nlp.vocab[w2]

STOP_WORDS = spacy.lang.en.stop_words.STOP_WORDS

title = "Performing a standard RHEL 9 installation"
subtitle = "Installing RHEL 9 using the graphical user interface"
abstract = "This document is for users who want to perform a standard RHEL 9 installation using the graphical user interface."
o = "This document describes common disaster scenarios that threaten an IdM deployment, along with methods to mitigate those situations through replication, Virtual Machine snapshots, and backups."

# adds stop words
nlp.Defaults.stop_words |= {"rhel","8","9"}

# removes stop words
# nlp.Defaults.stop_words -= {"stop", "word"}

#print(subtitle.similarity(abstract))
#print(nlp.Defaults.stop_words)


def process_text(text):
    doc = nlp(text.lower())
    result = []
    for token in doc:
        if token.text in nlp.Defaults.stop_words:
            continue
        if token.is_punct:
            continue
        if token.lemma_ == '-PRON-':
            continue
        result.append(token.lemma_)
    return " ".join(result)


def calculate_similarity(text1, text2):
    base = nlp(process_text(text1))
    compare = nlp(process_text(text2))
    return base.similarity(compare)




print(calculate_similarity(title, subtitle))








