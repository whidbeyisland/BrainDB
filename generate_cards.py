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
import pandas as pd
import uuid
import time

from config import userid
from query_executor import QueryExecutor

# User Changeable Options
#
flashcards_needed = 10 # change for more cards
default_card_text_file = 'default_card_source.txt'

####

def get_options():
    deck_name   = ''
    path_cwd = os.getcwd()

    try:
      body      = sys.argv[2]
      deck_name = sys.argv[4]
    except Exception as e:
      print('Body or Deck_Name not supplied. Using default name')
      body = load_default_card_text()

    options = dict( body        = body,
                    deck_name   = deck_name,
                    path_cwd    = path_cwd,
                    flashcards_needed = flashcards_needed)
    return options 

def load_default_card_text():
    with open(default_card_text_file) as f:
        body = f.read()
        return body

options = get_options()

# This next block takes 10-20 seconds. Want to speed it up by having the BERT model already loaded, but cannot
# figure out how to get BERT to accept the pre-saved model. However, this time delay is still improved over the
# >1 minute that it took before switching to "model='distilbert-base-uncased'"

def get_sentences(options):
    bert_path = os.path.join(options['path_cwd'], 'pkls', 'bert', 'pytorch_model')
    #bert_model = BertModel.from_pretrained('distilbert-base-uncased')
    #bert_model = BertModel.from_pretrained('distilbert-base-uncased', cache_dir='.cache/')
    bert_model = Summarizer(model='distilbert-base-uncased')
    #bert_sum = Summarizer(bert_model)
    bert_model_output = bert_model(options['body'], min_length=60, num_sentences=options['flashcards_needed'])
    bert_summary_text = ''.join(bert_model_output)
    # TODO: handle non-period sentence endings
    #
    bert_summary_sentences = bert_summary_text.split('. ') 
    bert_summary_sentences = [s.rstrip() for s in bert_summary_sentences]
    return bert_summary_sentences

bert_summary_sentences = get_sentences(options)

for i in range(0, len(bert_summary_sentences) - 1):
  bert_summary_sentences[i] += '.'

bert_summary_sentences_string = '\n'.join(bert_summary_sentences)
print(bert_summary_sentences_string)

# If the user has not provided a deck name, attempt to set a default one now, based on the first sentence. Otherwise, it
# has been initialized as a basic Guid.

if options['deck_name'] == '':
  try:
    options['deck_name'] = bert_summary_sentences[0][:30]
  except:
    options['deck_name'] = uuid.uuid4().hex

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

# print(find_keyword_in_sentence('My name is Wolfgang and I was born in 1990 in Berlin', True, True, True))

# Defining a function to actually cloze out that keyword, which we chose in the above function:

def sentence_clozed(sentence, nums_allowed, persons_allowed, places_allowed):
  _keyword = find_keyword_in_sentence(sentence, nums_allowed, persons_allowed, places_allowed)
  keyword_categ = _keyword[1]
  _keyword = _keyword[0]
  keyword_caps = _keyword[0].upper() + _keyword[1:]
  sentence_new = sentence.replace(_keyword, '___' + keyword_categ)
  sentence_new = sentence_new.replace(keyword_caps, '___' + keyword_categ)
  return [sentence_new, _keyword]

# print(sentence_clozed('My name is Wolfgang and I was born in Berlin in 1990', True, True, True))

# Whew! Now it's finally time to get your cloze-deleted cards. You can run this cell multiple times to get the same sentences with different keywords clozed out.

sentences_clozed = []
for i in range(0, len(bert_summary_sentences)):
  # cloze out the keyword in each sentence
  sentences_clozed.append(sentence_clozed(bert_summary_sentences[i], True, True, True))
# print(sentences_clozed)

# ----------------------STORAGE---------------------------

# Save it all as a DataFrame

deck_df = pd.DataFrame(sentences_clozed, columns = ['Front', 'Back'])
deck_path = os.path.join(options['path_cwd'], 'files', 'decks', options['deck_name'] + '.csv')
deck_df.to_csv(deck_path)
print(deck_df)

# Also store deck on RDS SQL Server instance

q = QueryExecutor()

deck_id_sql = uuid.uuid4()
# query_string = 'INSERT INTO TestTable VALUES (8)'
query_string = '''
INSERT INTO Decks (Id, UserId, DeckName, CreatedDate, ModifiedDate) VALUES (
  \'%s\',
  \'%s\',
  \'%s\',
  GETDATE(),
  GETDATE()
);
''' % (deck_id_sql, userid, options['deck_name'])
q.execute_insert_query(query_string)

# len(sentences_clozed)
for i in range(0, 5):
  try:
    time.sleep(1)
    front = sentences_clozed[i][0]
    front.replace('\'', '\\\'')
    back = sentences_clozed[i][1]
    back.replace('\'', '\\\'')
    query_string = '''
INSERT INTO Cards (DeckId, Front, Back, CreatedDate, ModifiedDate) VALUES (
  \'%s\',
  \'%s\',
  \'%s\',
  GETDATE(),
  GETDATE()
);
''' % (deck_id_sql, front, back)
    q.execute_insert_query(query_string)
  except Exception as e:
    print(e)

print('Backed up to Amazon RDS')