from preprocessor import titles, authors, descriptions, DoPs
from tfidf import tokenizer, tf, idf
import numpy as np
import math
import itertools

# A dictionary which selects the list of docs to use based on type of search selected by user
options_dict = {
    1: titles,
    2: list(authors.values()),
    3: descriptions,
    4: DoPs
}

def query_tokenizer(query):
    """
    Method to tokenize the give user query
    :param query: query string read from user input
    :return: List of tokens formed from the query
    """
    query_tokens = tokenizer(query)
    return query_tokens

# function returns a list of tf-idf values of give
def query_vectorizer(query, docs):
    """
    Method to form the tf-idf vector representing query
    :param query: query string read from user input
    :param docs: list of all documents based on the type of search selected
    :return: a list which represents the tf-idf vector of query
    """
    qtfidf = []
    query_tokens = query_tokenizer(query)
    for qtoken in query_tokens:
        qtfidf.append(tf(qtoken, query_tokens)*idf(qtoken, docs))
    return qtfidf

# function returns 
def doc_vectorizer(docs, query_tokens):
    """
    Method to form the tf-idf vector for each doc and store the vector as a value in a dictionary with key as doc
    :param docs: list of all documents based on the type of search selected
    :param query_tokens: tokens formed on the query string read from user input
    :return: a dict which represents the tf-idf vectors of each doc stored as value against the doc as key
    """
    docs_dict = {}
    for doc in docs:
        # print(doc)
        doc_tokens = tokenizer(doc)
        # print(doc_tokens)
        doc_tfidf = []

        for qtoken in query_tokens:
            if qtoken in doc_tokens:
                # if option == 3:
                doc_tfidf.append(tf(qtoken, doc_tokens)*idf(qtoken, docs))
                # elif option == 1:
                #     doc_tfidf.append(tf(qtoken, doc_tokens)*lookup_titles[qtoken])
                # elif option == 2:
                #     doc_tfidf.append(tf(qtoken, doc_tokens)*lookup_authors[qtoken]) 
            else:
                doc_tfidf.append(0)
        docs_dict[doc] = doc_tfidf
    return docs_dict


def normalize (vec):
    """
    Method to find the normalized form of a vector
    :param vec: a given tf-idf vector
    :return: the vector in normalized form
    """
    summ = 0
    for v in vec:
        summ += v**2
    summ = math.sqrt(summ)
    if (summ != 0):
        vec = [float(v)/summ for v in vec]
    return vec

def cosine_similarity(v1, v2):
    """
    Method to find the dot product of two vectors
    :param v1: a given tf-idf vector
    :param v2: a given tf-idf vector
    :return: the dot product/cosine similarity of two vectors
    """
    return np.dot(v1, v2)

def search_result (query, option):
    """
    Method to find the top results to be given to user as output based on query and search type
    :param query: query string read from user input
    :param option: search type
    :return: list or dictionary of the top results of a particular search
    """
    docs =  options_dict[option]

    # Year of Publication does not use TF-IDF, it directly prints 10 (or all of them if they are less than 10) articles released in the given year
    if option == 4:
        dop_dict = {}
        q = int(query)
        for key, val in DoPs.items():
                if q == val and key not in dop_dict.keys():
                    dop_dict[key] = val
        if dop_dict == {}:
            print('Nothing published in the chosen year.')
        return dop_dict


    else:
        # Converting the query into a TF-IDF vector and normalising it
        query_vector = query_vectorizer(query, docs)
        query_vector = normalize(query_vector)
        
        # Creating a dictionary that holds the title as key and TF-IDF as value
        docs_dict = doc_vectorizer(docs, query_tokenizer(query))
        # Normalizing the above
        for doc in docs:
            docs_dict[doc] = normalize(docs_dict[doc])
        
        # Creating a final dictionary that would print the title and corresponding cosine similarity value
        final_dict = {}
        for doc in docs:
            final_dict[doc] = (cosine_similarity(query_vector, docs_dict[doc]))
            
        # if Titles, sort in descending order of cosine values and print top 10
        if option == 1:
            final_dict = sorted(final_dict.items(), key=lambda kv: kv[1], reverse=True)
            return (final_dict[:10])

        # if Authors or Description, link authors/descriptions to title, cosine dictionary and print top 10
        elif option == 3 or option == 2:
            descrip_dict = final_dict
            descrip_dict = sorted(descrip_dict.items(), key=lambda kv: kv[1], reverse=True)
            final_dict = dict(zip(titles, list(final_dict.values())))
            final_dict = list(sorted(final_dict.items(), key=lambda kv: kv[1], reverse=True))
            return (dict(zip(final_dict[:10], descrip_dict[:10])))