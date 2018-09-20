#import os for path to dataset
#import nltk for tokenizing and n-grams
import os, nltk
# nltk.download('punkt', quiet=True)

#import tf-idf functions from tfidf.py
from tfidf import tokenizer, tf, idf

#ElementTree is used to parse XML files
from xml.etree import ElementTree

#Dataset and its location (which is the current working directory)
file_name = 'nasa.xml'
full_file = os.path.abspath(os.path.join('', file_name))

dom = ElementTree.parse(full_file)

'''
XML has <datasets> tag which is a global, all-encompassing tag.
<datasets> has a <dataset> tag which holds information about a Research Paper,
which subsequently has <title> tags for the name of the title, <author> tags for the author's name,
<description> tags for an abstract of the paper and a <year> tag which holds the year of publication
'''

data = dom.findall('dataset')
titles = []         # List containing all the titles stored as strings
authors = {}        # A Dictionary containing Titles of the paper as keys and a list of Authors as values
descriptions = []   # A list containing a Description corresponding to each Title
DoPs = {}           # A dictionary containing 


#Iterate through each piece of data, i.e., each Research Paper
for d in data:

        # Title
        title = d.find('title').text    # .text returns the text of the title
        titles.append(title)            # append it to the 'titles' array
        
        # Authors
        authorList = []                 # list that holds all the authors for a given paper

        # find the authors in the XML file, can be either under .../other/author or .../journal/other
        athrs = d.findall('reference/source/other/author')
        if(not len(athrs)):
            athrs = d.findall('reference/source/journal/author')

        # iterate through all the authors for a given document
        for author in athrs:

            authorName = 'Unknown'      # set it to Unknown initially so that if the author information is NA, this will be default

            # find author initials and add authors' last name to a string
            if(author != None):
                initials = author.findall('initial')
                authorName = ''
                for i in initials:
                    authorName += i.text
                authorName += ' ' + author.find('lastName').text
            
            # append the above string containing the authors' initials and last name to a list
            authorList.append(authorName)

        # store the list of authors as a string value for a title key in the authors dictionary
        authors[title] = (' '.join(authorList))
        
        # Description

        # description is stored in .../description/para tags in the XML file
        des = d.find('descriptions/description/para')

        # set description to default to 'No Description'
        description = 'No Description'

        # extract text from the element
        if (des != None):
            description = des.text

        # append to the descriptions list
        descriptions.append(description)
        

        # Year of Publication

        if title == None:
            continue
        
        # year of publication can be under .../other/date/year or .../journal/date/year
        dop = d.find('reference/source/other/date/year')
        if (dop is None):
            dop = d.find('reference/source/journal/date/year')

        # try to insert into DoPs dictionary else set date of publication as the year 3000
        if (dop is not None):
            try:
                DoPs[title] = int(dop.text)
            except:
                DoPs[title] = 3000
        else:
            DoPs[title] = 3000

        if (dop is None):
            DoPs[title] = 3000
# print(titles)
# print(list(authors.values()))