# necessary imports
import pandas as pd
import nltk
import re
from textblob import TextBlob
import heapq
from tqdm import tqdm
import language_tool_python

punctuation = '!"#$%&\()*+,-/:;<=>?@[\\]^_`{|}~…' # removed fullstop and single quote
emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", re.UNICODE)

# text preprocessing function
def text_process(text):
    """
    ### Text preprocessing steps:
    - remove links
    - remove hashtags
    - remove special characters (preserving fullstops since they mark end of sentence and we're doing summarization
      based off of sentence weights, also preserve single quotes)
    - remove numbers
    - remove emojis and emoticons
    - correct spelling
    - strip the text
    - put a fullstop at the end of each preprocessed tweet if there is not one
    - make the first letter of preprocessed tweets a capital letter if it isn't the case
    """

    text = re.sub(r'https?://\S+|www\.\S+', repl=r'', string=text)
    text = text.split()
    text = ' '.join([word for word in text if not word.startswith("#")])
    text = ''.join([c for c in text if c not in punctuation])
    text = ''.join([i for i in text if not i.isdigit()])
    text = re.sub(emoj, '', text)
    text = str(TextBlob(text).correct())
    text = text.strip()
    if not text.endswith("."):
        text = text + "."
    if not text[0].isupper():
        text = text[0].upper() + text[1:]
    return text

# text processing function preserving digits
def text_processdig(text):
    text = re.sub(r'https?://\S+|www\.\S+', repl=r'', string=text)
    text = text.split()
    text = ' '.join([word for word in text if not word.startswith("#")])
    text = ''.join([c for c in text if c not in punctuation])
    text = re.sub(emoj, '', text)
    text = str(TextBlob(text).correct())
    text = text.strip()
    if not text.endswith("."):
        text = text + "."
    if not text[0].isupper():
        text = text[0].upper() + text[1:]
    return text


def get_summary(df):

    # designing documents of preprocessed texts joined together
    doc_without_numbers = ""

    for tweet in tqdm(df.text, desc="Designing preprocessed document:"):
        tweet = text_process(tweet)
        doc_without_numbers += tweet

    doc_with_numbers = ""

    for tweet in tqdm(df.text, desc="Designing document preserving numbers:"):
        tweet = text_processdig(tweet)
        doc_with_numbers += tweet

    # converting document to recognizable sentences
    sentence_list = nltk.sent_tokenize(doc_with_numbers)

    # find weighted frequency of occurence of each word(using preprocessed document; without numbers)
    stopwords = nltk.corpus.stopwords.words('english')

    word_frequencies = {}
    for word in nltk.word_tokenize(doc_without_numbers):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1

    # to find the weighted frequency, we can simply divide the number of occurances of
    # all the words by the frequency of the most occurring word

    maximum_frequncy = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word] / maximum_frequncy)

    # calculating sentence scores
    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) > 3 & len(sent.split(' ')) < 20:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]


    # Getting summary from sentences with higher score than others
    #Taking care of shorter and extremely longer summaries
    #   - summaries below 3000 characters
    #   - summaries over  4500 characters
    n = 5

    summary_sentences = heapq.nlargest(n, sentence_scores, key=sentence_scores.get)
    summary = ' '.join(summary_sentences)

    if len(summary) < 1500:
        while len(summary) < 2500:
            if n + 3 < len(sentence_list):
                n = n + 3
            summary_sentences = heapq.nlargest(n, sentence_scores, key=sentence_scores.get)

    summary = ' '.join(summary_sentences)


    # correcting errors in sentences
    tool = language_tool_python.LanguageTool('en-US')
    summary = tool.correct(summary)

    return summary