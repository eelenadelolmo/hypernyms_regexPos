import en_core_web_lg
import re

texto = "I am only testing the script with this very short sentence, advanced searches should be tested with long texts or a longer sentence"
consulta = "(_pos::DET_)? ((_tag::RB_)? (_text::long(er)?_|_text::short_))? _pos::NOUN_"

nlp = en_core_web_lg.load()
doc = nlp(texto)
print(doc.text)

str_sentence = ""

# Selected: text, lemma_, pos_, tag_, dep_, head.text
for token in doc:
    # print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop, token.head.text)
    str_sentence += token.text + "::" + token.lemma_ + "::" + token.pos_ + "::" + token.tag_ + "::" + token.dep_ + "::" + token.head.text + "____"
str_sentence = str_sentence[:-4]

print(str_sentence)


# Allowed searches consist of a sequence of key-value pairs separated by :: and between underscores (_) containing the feature names and values
# All the expressive power of regular expressions is allowed within searches
# Blank spaces can be used as desired, as they will be ignored for the string matching

# Example: (_pos::DET_)? ((_tag::RB_)? (_text::longer_|_text::long_|_text::short_))? _pos::NOUN_

# Allowed feature names are:
# text (text): literal string
# lemma (lemma_): lemmatized string
# pos (pos_): coarse morphological tag
# tag (tag_): fine-grained morphological tag
# dep (dep_): dependency name
# head (head.text): text of dependency root

# The list of values is available here: https://spacy.io/models/en#en_core_web_lg-labels

feat_txt_list = list()

for match in re.finditer("_(.+?)::(.+?)_", consulta):
    feat_txt = (match.group(1), match.group(2))
    feat_txt_list.append(feat_txt)

print(feat_txt_list)
regex_reconstructed = consulta

for f_t in feat_txt_list:

    feat = f_t[0]
    txt = f_t[1]

    if feat == 'text':
        n = 0
    elif feat == 'lemma':
        n = 1
    elif feat == 'pos':
        n = 2
    elif feat == 'tag':
        n = 3
    elif feat == 'dep':
        n = 4
    elif feat == 'head':
        n = 5

    regex_reconstructed = re.sub('_' + feat + '::' + re.escape(txt) + '_', '(____|^)([^_]*?::){' + str(n) + '}' + txt + '(::|____)[^_]*?', regex_reconstructed)

# Deleting the last .*? metacharacters and blank spaces, adding final matching requirements
regex_reconstructed = regex_reconstructed[:-6]
regex_reconstructed += '[^_]*?(____|$)'
regex_reconstructed = re.sub(' ', '', regex_reconstructed)

print(regex_reconstructed)
