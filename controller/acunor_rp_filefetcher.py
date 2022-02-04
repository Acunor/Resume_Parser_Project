import PyPDF2 
import docx
import docx2txt
import os
from spacy.matcher import PhraseMatcher
from os import listdir
from os.path import isfile, join
from io import StringIO
import pandas as pd
from collections import Counter
from collections import Counter
import en_core_web_sm
nlp = en_core_web_sm.load()
from spacy.matcher import PhraseMatcher

from acunor_rp_parse import Parser


class FileFetcher(object):
    
    def __init__(self):
        self.parser=Parser()
    
    def fetch_and_parse_file(self,myfile):  
        split_tup = os.path.splitext(myfile)
        file_extension = split_tup[1]
        if file_extension=='.pdf':
            text=self.fetch_pdf_file(myfile)
            self.parser.parse_and_save_text(myfile, text)
        elif file_extension=='.docx':
            text=self.fetch_pdf_file(file)
            text=self.parser.parse_text(text)
        else:
            print("Invalid Formate")
                
                
#         mypath= r'C:\Users\admin\Desktop\resumes\datascience'
#         myfile=r''C:\Users\admin\Desktop\resumes\datascience\'
#         onlyfiles = [os.path.join(mypath, f) for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
        
#         i=0
#         final_database=pd.DataFrame()
#         while i < len(onlyfiles):
#             file = onlyfiles[i] 
#             split_tup = os.path.splitext(file)
#             file_extension = split_tup[1]
#             if file_extension=='.pdf':
#                 text=self.fetch_pdf_file(file)
#                 self.parser.parse_and_save_text(file, text)
#             elif file_extension=='.docx':
#                 text=self.fetch_pdf_file(file)
#                 text=self.parser.parse_text(text)
#             else:
#                 print("Invalid Formate")
#             i+=1    
    
#     def fetch_and_parse_file(self):     
#         split_tup = os.path.splitext('resume.pdf')
#         file_extension = split_tup[1]
#         if file_extension=='.pdf':
#             text=self.fetch_pdf_file('resume.pdf')
#             return self.parser.parse_text(text)
#         elif file_extension=='.docx':
#             text=self.fetch_pdf_file()
#             return self.parser.parse_text(text)
#         else:
#             print("Invalid Formate") 
       
    def fetch_pdf_file(self,file):
        pdfFileObj = open(file,'rb')               #open allows you to read the file
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)   #The pdfReader variable is a readable object that will be parsed
        num_pages = pdfReader.numPages                 #discerning the number of pages will allow us to parse through all the pages
        count = 0
        text = ""
        while count < num_pages:                       #The while loop will read each page
            pageObj = pdfReader.getPage(count)
            count +=1
            text += pageObj.extractText()
        return text
    
    def fetch_docx_file(self):
        temp = docx2txt.process('Bhargavi Angular JS Developer.docx')
        text = [line.replace('\t', ' ') for line in temp.split('\n') if line]
        return ' '.join(text)
    
    def fetch_doc_file(self):
        pass
    
    
    


           