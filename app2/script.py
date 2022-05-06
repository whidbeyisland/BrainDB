# from transformers.models.bert.modeling_bert import BertModel, BertForMaskedLM
from transformers.models.bert.modeling_bert import BertModel, BertForMaskedLM
import transformers
from summarizer import Summarizer,TransformerSummarizer
# summarizer.bert.TransformerSummarizer
from transformers import AutoTokenizer, AutoModelForTokenClassification, AutoModel
from transformers import pipeline
import random
import pickle
import os
import sys

path_cwd = os.getcwd()

body = ''
try:
  body = sys.argv[2]
except Exception as e:
  print(e)
  body = '''
        Scientists say they have discovered a new species of orangutans on Indonesia’s island of Sumatra.
  The population differs in several ways from the two existing orangutan species found in Sumatra and the neighboring island of Borneo.
  The orangutans were found inside North Sumatra’s Batang Toru forest, the science publication Current Biology reported.
  Researchers named the new species the Tapanuli orangutan. They say the animals are considered a new species because of genetic, skeletal and tooth differences.
  Michael Kruetzen is a geneticist with the University of Zurich who has studied the orangutans for several years. He said he was excited to be part of the unusual discovery of a new great ape in the present day. He noted that most great apes are currently considered endangered or severely endangered.
  Gorillas, chimpanzees and bonobos also belong to the great ape species.
  Orangutan – which means person of the forest in the Indonesian and Malay languages - is the world’s biggest tree-living mammal. The orange-haired animals can move easily among the trees because their arms are longer than their legs. They live more lonely lives than other great apes, spending a lot of time sleeping and eating fruit in the forest.
  The new study said fewer than 800 of the newly-described orangutans exist. Their low numbers make the group the most endangered of all the great ape species.
  They live within an area covering about 1,000 square kilometers. The population is considered highly vulnerable. That is because the environment which they depend on is greatly threatened by development.
  Researchers say if steps are not taken quickly to reduce the current and future threats, the new species could become extinct “within our lifetime.”
  Research into the new species began in 2013, when an orangutan protection group in Sumatra found an injured orangutan in an area far away from the other species. The adult male orangutan had been beaten by local villagers and died of his injuries. The complete skull was examined by researchers.
  Among the physical differences of the new species are a notably smaller head and frizzier hair. The Tapanuli orangutans also have a different diet and are found only in higher forest areas.
  There is no unified international system for recognizing new species. But to be considered, discovery claims at least require publication in a major scientific publication.
  Russell Mittermeier is head of the primate specialist group at the International Union for the Conservation of Nature. He called the finding a “remarkable discovery.” He said it puts responsibility on the Indonesian government to help the species survive.
  Matthew Nowak is one of the writers of the study. He told the Associated Press that there are three groups of the Tapanuli orangutans that are separated by non-protected land.He said forest land needs to connect the separated groups.
  In addition, the writers of the study are recommending that plans for a hydropower center in the area be stopped by the government.
  It also recommended that remaining forest in the Sumatran area where the orangutans live be protected.
  I’m Bryan Lynn.

            '''
print('body: ' + body)

# To start with, let's make 10 flashcards.

sentences_needed = 10

# This next block takes 10-20 seconds. Want to speed it up by having the BERT model already loaded, but cannot
# figure out how to get BERT to accept the pre-saved model. However, this time delay is still improved over the
# >1 minute that it took before switching to "model='distilbert-base-uncased'"

bert_path = os.path.join(path_cwd, 'pkls', 'bert', 'pytorch_model')
#bert_model = BertModel.from_pretrained('distilbert-base-uncased')
#bert_model = BertModel.from_pretrained('distilbert-base-uncased', cache_dir='.cache/')
bert_model = Summarizer(model='distilbert-base-uncased')
#bert_sum = Summarizer(bert_model)

bert_summary_text = ''.join(bert_model(body, min_length=60, num_sentences=sentences_needed))

bert_summary_sentences = bert_summary_text.split('. ')
bert_summary_sentences = [sent.rstrip() for sent in bert_summary_sentences]
for i in range(0, len(bert_summary_sentences) - 1):
  bert_summary_sentences[i] += '.'
bert_summary_sentences_string = '\n'.join(bert_summary_sentences)
print(bert_summary_sentences_string)

# From here on out it's faster.

pn_tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
pn_model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")

nlp = pipeline("ner", model=pn_model, tokenizer=pn_tokenizer)

# Defining a function to randomly pick a keyword to cloze out in each sentence:

def find_keyword_in_sentence(sentence, nums_allowed, persons_allowed, places_allowed):
  _words = sentence.rstrip().split()
  _words = [[w, ''] for w in _words]

  #-------------------------------------
  # eliminate invalid keywords, if necessary

  # numbers
  _words_numbers = list(filter(lambda w: w[0].isnumeric(), _words))
  _words = list(filter(lambda w: w not in _words_numbers, _words))
  for j in range(0, len(_words_numbers)):
    _words_numbers[j][1] = ' [NUMBER]'
  if nums_allowed == True:
    _words = _words + _words_numbers

  ner_results = nlp(sentence)

  # people's names
  _words_persons = []
  for j in range(0, len(ner_results)):
    if ner_results[j]['entity'] == 'B-PER':
      _words_persons.append([ner_results[j]['word'], ''])
  _words = list(filter(lambda w: w not in _words_persons, _words))
  for j in range(0, len(_words_persons)):
    _words_persons[j][1] = ' [PERSON]'
  if persons_allowed == True:
    _words = _words + _words_persons

  # place names
  _words_places = []
  for j in range(0, len(ner_results)):
    if ner_results[j]['entity'] == 'B-LOC':
      _words_places.append([ner_results[j]['word'], ''])
  _words = list(filter(lambda w: w not in _words_places, _words))
  for j in range(0, len(_words_places)):
    _words_places[j][1] = ' [PLACE]'
  if places_allowed == True:
    _words = _words + _words_places

  # short words (that don't fall into specific categories e.g. numbers)
  _words = list(filter(lambda w: len(w[0]) >= 5 or w[1] != '', _words))
  #-------------------------------------

  _keyword = _words[random.randint(0, len(_words) - 1)]
  return _keyword

print(find_keyword_in_sentence('My name is Wolfgang and I was born in 1990 in Berlin', True, True, True))

# Defining a function to actually cloze out that keyword, which we chose in the above function:

def sentence_clozed(sentence, nums_allowed, persons_allowed, places_allowed):
  _keyword = find_keyword_in_sentence(sentence, nums_allowed, persons_allowed, places_allowed)
  keyword_categ = _keyword[1]
  _keyword = _keyword[0]
  keyword_caps = _keyword[0].upper() + _keyword[1:]
  sentence_new = sentence.replace(_keyword, '___' + keyword_categ)
  sentence_new = sentence_new.replace(keyword_caps, '___' + keyword_categ)
  return [sentence_new, _keyword]

print(sentence_clozed('My name is Wolfgang and I was born in Berlin in 1990', True, True, True))

# Whew! Now it's finally time to get your cloze-deleted cards. You can run this cell multiple times to get the same sentences with different keywords clozed out.

sentences_clozed = []
for i in range(0, len(bert_summary_sentences)):
  # cloze out the keyword in each sentence
  sentences_clozed.append(sentence_clozed(bert_summary_sentences[i], True, True, True))
print(sentences_clozed)