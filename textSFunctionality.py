import re
import json
import spacy
import tensorflow as tf
import numpy as np
from collections import Counter



MAX_LEN = 798

nlp = spacy.load('en_core_web_sm')

# Load Tensorflow Tokenizer From tokenizer.json
with open('tokenizer.json', 'r') as json_file:
    tokenizer_data = json.load(json_file)

tokenizer = tf.keras.preprocessing.text.tokenizer_from_json(tokenizer_data)
model = tf.keras.models.load_model('TS.h5')

def cleanText(text):
    text = str(text)
    text = re.sub(r'[^\w\s]', '', text)
    text = text.lower()
    return text

def extractive_summary(text, top_n=5):
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]
    word_freq = Counter([token.lemma_ for token in doc if not token.is_stop and not token.is_punct])
    max_freq = max(word_freq.values(), default=1)

    for word in word_freq:
        word_freq[word] = word_freq[word] / max_freq

    sentence_scores = {}
    for sent in doc.sents:
        for word in sent:
            if word.lemma_ in word_freq:
                sentence_scores[sent] = sentence_scores.get(sent, 0) + word_freq[word.lemma_]

    summarized_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:top_n]
    summary = ' '.join([sent.text for sent in summarized_sentences])

    return summary

def generateText(input_text):
    preprocessed_text = re.sub(r'\w*\d\w*', '', input_text).lower()
    tokenized_text = tokenizer.texts_to_sequences([preprocessed_text])
    tokenized_text = tf.keras.preprocessing.sequence.pad_sequences(tokenized_text, maxlen=MAX_LEN, padding='post')
    input_summary = extractive_summary(input_text)
    summary_tokenized = tokenizer.texts_to_sequences([input_summary])
    summary_tokenized = tf.keras.preprocessing.sequence.pad_sequences(summary_tokenized, maxlen=MAX_LEN, padding='post')
    prediction = model.predict([tokenized_text, summary_tokenized])
    predicted_sequence = np.argmax(prediction, axis=-1)
    final_output = ' '.join([tokenizer.index_word[i] for i in predicted_sequence[0] if i != 0 and tokenizer.index_word.get(i, '') != '<OOV>'])
    return final_output 