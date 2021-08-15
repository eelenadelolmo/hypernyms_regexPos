import en_core_web_lg
import re

nlp = en_core_web_lg.load()
doc = nlp("I am only testing with this short sentence")
print(doc.text)

str_sentence = ""

# Selected: text, lemma_, pos_, tag_, dep_, head.text
for token in doc:
    #print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop, token.head.text)
    str_sentence += token.text + "::" + token.lemma_ + "::" + token.pos_ + "::" + token.tag_ + "::" + token.dep_ + "::" + token.head.text + "____"
str_sentence = str_sentence[:-4]

print(str_sentence)


# Allowed searches consist of:
# A sequence of key-value pairs separated by :: with the feature names and values within a regular expression
# Example: (pos::DET)? text::sentence

# Allowed feature names are:
# text (text): literal string
# lemma (lemma_): lemmatized string
# pos (pos_): coarse morphological tag
# tag (tag_): fine-grained morphological tag
# dep (dep_): depedency name
# head (head.text): text of dependency root

# The list of values is available here: https://spacy.io/models/en#en_core_web_lg-labels

# def searcher(search, str):

consulta = "(_pos::DET_)? _text::short_ _text::sentence_"
consulta_parsed = list()

for token in consulta.split():
    match = re.search("(.*?)_(.+?)::(.+?)_(.*)", token)
    regPre_feat_txt_regPost = (match[1], match[2], match[3], match[4])
    consulta_parsed.append(regPre_feat_txt_regPost)

regex_reconstructed = ''

for token in consulta_parsed:

    regPre = token[0]
    txt = token[2]
    regPost = token[3]

    if token[1] == 'text':
        n = 0
    elif token[1] == 'lemma':
        n = 1
    elif token[1] == 'pos':
        n = 2
    elif token[1] == 'tag':
        n = 3
    elif token[1] == 'dep':
        n = 4
    elif token[1] == 'head':
        n = 5

    regex_reconstructed += regPre + '(____|^)([^_]*?::){' + str(n) + '}' + txt + '.*?' + regPost

# Deleting the last ____ separator
regex_reconstructed = regex_reconstructed[:-3]

print(regex_reconstructed)