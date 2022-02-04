import spacy
from spacy.matcher import Matcher
import re
import nltk
import re
import spacy
import json
from nltk.corpus import stopwords
import pandas as pd
import en_core_web_sm
from spacy.matcher import PhraseMatcher
from collections import Counter
import os
from os import listdir
from os.path import isfile, join
from io import StringIO
import matplotlib.pyplot as plt

import sys
sys.path.append(r"C:\Users\admin\Projects\ResumeParser\model")
from acunor_rp_employee_details import EmployeeDetails

sys.path.append(r"C:\Users\admin\Projects\ResumeParser\data_provider")
from acunor_rp_dataprovider import CouchdbProvider

class Parser(object):
         
    def __init__(self):
        pass
    
    def parse_and_save_text(self,file,text):
        cdbp=CouchdbProvider()
        employeedetails=self.parse_text(file,text)
        cdbp.save_data(employeedetails)
        
        
    def parse_text(self,file,text):
        skill_frequency=self.create_profile(file,text)
        print(skill_frequency)
        name=self.extract_name(text)
        mobile=self.extract_mobile_number(text)
        email=self.extract_email(text)
        skills=self.extract_skills(text)        
        education=self.extract_education(text)
        #print(name,mobile,email,skills,education) 
        employeedetails=EmployeeDetails(name,mobile,email,skills,education)   
        return employeedetails
#         jdata=json.dumps(employeedetails.__dict__)
#         print(dir(employeedetails))
#         print('\n')
#         print(jdata)
#         return jdata
        
    
    def extract_name(self,name):   
        nlp = spacy.load('en_core_web_sm') # load pre-trained model
        matcher = Matcher(nlp.vocab)       # initialize matcher with a vocab
        nlp_text = nlp(name)
        pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]  # First name and Last name are always Proper Nouns
        matcher.add('NAME',[pattern])       
        matches = matcher(nlp_text)
        for match_id, start, end in matches:
            span = nlp_text[start:end]
            return span.text
        
    def extract_mobile_number(self,mobile):
        phone = re.findall(re.compile(r'(?:(?:\+?([1-9]|[0-9][0-9]|[0-9][0-9][0-9])\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([0-9][1-9]|[0-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?'), mobile)
        if phone:
            number = ''.join(phone[0])
            if len(number) > 10:
                return '+' + number
            else:
                return number
            
    def extract_email(self,email):
        email = re.findall("([^@|\s]+@[^@]+\.[^@|\s]+)", email)
        if email:
            try:
                return email[0].split()[0].strip(';')
            except IndexError:
                return None
       
    def extract_skills(self,skills):
        SKILLS_DB = ['linq','sql server','agile','scrun','waterfall','jams','azure','sql','jira','spotlight']
        stop_words = set(nltk.corpus.stopwords.words('english'))
        word_tokens = nltk.tokenize.word_tokenize(skills)
        # remove the stop words
        filtered_tokens = [w for w in word_tokens if w not in stop_words]
        # remove the punctuation
        filtered_tokens = [w for w in word_tokens if w.isalpha()]
        # generate bigrams and trigrams (such as artificial intelligence)
        bigrams_trigrams = list(map(' '.join, nltk.everygrams(filtered_tokens, 2, 3)))
        # we create a set to keep the results in.
        found_skills = set()
        # we search for each token in our skills database
        for token in filtered_tokens:
            if token.lower() in SKILLS_DB:
                found_skills.add(token)
        # we search for each bigram and trigram in our skills database
        for ngram in bigrams_trigrams:
            if ngram.lower() in SKILLS_DB:
                found_skills.add(ngram)
        found_skills=list(found_skills)
        return found_skills
    
    def extract_education(self,edu):
        nlp = spacy.load('en_core_web_sm')  # load pre-trained model
        STOPWORDS = set(stopwords.words('english'))  # Grad all general stop words
        EDUCATION = ['BE','B.E.','B.E','BS','B.S','ME','M.E','M.E.','MS','M.S','BTECH','B.TECH','M.TECH','MTECH','SSC','HSC','CBSE','ICSE','X','XII']
        nlp_text = nlp(edu)
        # Sentence Tokenizer
        #nlp_text = [sent.string.strip() for sent in nlp_text.sents]
        nlp_text = [sent.text.strip() for sent in nlp_text.sents]
        edu = {}
        # Extract education degree
        for index, text in enumerate(nlp_text):
            for tex in text.split():
                # Replace all special symbols
                tex = re.sub(r'[?|$|.|!|,]', r'', tex)
                if tex.upper() in EDUCATION and tex not in STOPWORDS:
                    edu[tex] = text + nlp_text[index + 1]
        # Extract year
        education = []
        for key in edu.keys():
            year = re.search(re.compile(r'(((20|19)(\d{2})))'), edu[key])
            if year:
                education.append((key, ''.join(year[0])))
            else:
                education.append(key)
        return education
    
    def create_profile(self,file,text):
        nlp = en_core_web_sm.load()
        import pandas as pd
        text = str(text)
        text = text.replace("\\n", "")
        text = text.lower()
        #below is the csv where we have all the keywords, you can customize your own
        keyword_dict = pd.read_csv(r'C:\Users\admin\Desktop\resumes\skills.csv')
        stats_words = [nlp(text) for text in keyword_dict['Statistics'].dropna(axis = 0)]
        NLP_words = [nlp(text) for text in keyword_dict['NLP'].dropna(axis = 0)]
        ML_words = [nlp(text) for text in keyword_dict['Machine Learning'].dropna(axis = 0)]
        DL_words = [nlp(text) for text in keyword_dict['Deep Learning'].dropna(axis = 0)]
        R_words = [nlp(text) for text in keyword_dict['R Language'].dropna(axis = 0)]
    #     python_words = [nlp(text) for text in keyword_dict['Python Language'].dropna(axis = 0)]
        Data_Engineering_words = [nlp(text) for text in keyword_dict['Data Engineering'].dropna(axis = 0)]

        matcher = PhraseMatcher(nlp.vocab)
        matcher.add('Stats', None, *stats_words)
        matcher.add('NLP', None, *NLP_words)
        matcher.add('ML', None, *ML_words)
        matcher.add('DL', None, *DL_words)
        matcher.add('R', None, *R_words)
    #     matcher.add('Python', None, *python_words)
        matcher.add('DE', None, *Data_Engineering_words)


        doc = nlp(text)

        d = []
        matches = matcher(doc)
        for match_id, start, end in matches:
            rule_id = nlp.vocab.strings[match_id]  # get the unicode ID, i.e. 'COLOR'
            span = doc[start : end]  # get the matched slice of the doc
            d.append((rule_id, span.text))
        keywords = "\n".join(f'{i[0]} {i[1]} ({j})' for i,j in Counter(d).items())

        ## convertimg string of keywords to dataframe    
        df = pd.read_csv(StringIO(keywords),names = ['Keywords_List'])
        df1 = pd.DataFrame(df.Keywords_List.str.split(' ',1).tolist(),columns = ['Subject','Keyword'])
        df2 = pd.DataFrame(df1.Keyword.str.split('(',1).tolist(),columns = ['Keyword', 'Count'])
        df3 = pd.concat([df1['Subject'],df2['Keyword'], df2['Count']], axis =1) 
        df3['Count'] = df3['Count'].apply(lambda x: x.rstrip(")"))

        base = os.path.basename(file)
        filename = os.path.splitext(base)[0]

        name = filename.split('_')
        name2 = name[0]
        name2 = name2.lower()
        ## converting str to dataframe
        name3 = pd.read_csv(StringIO(name2),names = ['Candidate Name'])

        dataf = pd.concat([name3['Candidate Name'], df3['Subject'], df3['Keyword'], df3['Count']], axis = 1)
        dataf['Candidate Name'].fillna(dataf['Candidate Name'].iloc[0], inplace = True)
        return(dataf)   
    
    
        