# import nltk for tokenizing and n-grams
import string, nltk

# import PorterStemmer for the Porter Stemmer Algorithm
from nltk.stem import PorterStemmer

# Download the list of english stopwords using nltk.download() and import them
# nltk.download('stopwords', quiet=True)
from nltk.corpus import stopwords

# word tokenizer and n-grams
from nltk import word_tokenize, ngrams

# import math for log and sqrt functions used in tf-idf calculations
import math


#Set Stopwords from NLTK
stops = set((stopwords.words('english')) + list(string.punctuation))


def freq(word, doc):
    '''
    Frequency Counter Function
    :param word: the word whose frequency is to be calculated
    :param doc: the document in which the frequency of the word is to be calculated
    :return: return the number of times word has appeared in doc
    '''
    return doc.count(word)


# function returns number of documents having given word    
def docshaving(word, docslist):
    '''
    Function to calculate the number of times a given word occurs in a given document set
    :param word: word whose frequency in the entire document set is to be calculated
    :param docslist: a list containing all documents pertaining to a selected search category
    :return: the count of the number of documents in docslist in which word occurs
    '''
    count = 0
    for doc in docslist:
        if word in doc.lower():
            count += 1
    return count
        
# function returns tf value of the given word in given document.    
def tf(word, doc):
    '''
    TF-Calculator Function
    This function calculates and returns the term frequency of a given word in a document
    :param word: the term for which tf is to be calculated
    :param doc: the document in which the term frequency must be checked for
    :return: return 1 + log(tf), i.e., the weight function that term frequency contributes to TF-IDF
    '''
    if freq(word, doc) is not 0:
        return (1 + math.log(freq(word, doc)))
    else:
        return 0
    
# function returns idf value of the given word in given list of documents.    
def idf(word, docslist):
    '''
    IDF-Calculator Function
    This function calculates and returns the Inverse Document Frequency of a given term
    :param word: the term for which idf is to be calculated
    :param docslist: a list of all the docs pertaining to the search category selected
    :return: log(N/df), i.e., IDF for N being the total number of documents and df being the document frequency of the term
    '''
    d = float(docshaving(word, docslist))
    N = len(docslist)
    if (d != 0):
        return (math.log(N/d))
    else:
        return 0

def stemmer(vector):
    '''
    Stemmer Function based on the Porter Stemmer Algorithm to stem words
    :param vector: the set of words to be stemmed
    :return: returns a stemmed version of vector
    '''
    stemmed = []
    stemmer = PorterStemmer()
    for item in vector:
        stemmed.append(stemmer.stem(item))
    return stemmed

# function returns list of tokens obtained from a string, including unigrams and bigrams
def tokenizer (doc):
    '''
    Tokenizer Function that splits a string and converts them into unigrams and bigrams
    :param doc: the string for which tokens have to be made
    :return: a list of tokens extracted from the string, including unigrams and bigrams
    '''
    doc_tokens = [i for i in word_tokenize(doc.lower()) if i not in stops]
    doc_tokens = stemmer(doc_tokens)
    unigram = [' '.join(gram) for gram in ngrams(doc_tokens, 1)] 
    bigram = [' '.join(gram) for gram in ngrams(doc_tokens, 2)]
    doc_tokens = list(set(unigram + bigram))
    return (doc_tokens)