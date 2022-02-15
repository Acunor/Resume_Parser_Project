from flask import Flask, render_template, request, flash, redirect, url_for
from registerform import RegisterForms
from loginform import LoginForms
from IPython.display import HTML
from werkzeug.utils import secure_filename

import PyPDF2 
import docx
import docx2txt
from spacy.matcher import PhraseMatcher
from os import listdir
from os.path import isfile, join
from io import StringIO
from collections import Counter
from collections import Counter
from spacy.matcher import PhraseMatcher



import os
import couchdb
import pandas as pd
import json



import sys
sys.path.append(r"C:\Users\admin\Projects\ResumeParser\data_provider")
from acunor_rp_dataprovider import CouchdbProvider

sys.path.append(r"C:\Users\admin\Projects\ResumeParser\controller")
from acunor_rp_filefetcher import FileFetcher

app=Flask(__name__)

app.config['SECRET_KEY']='nercuhko'

UPLOAD_FOLDER = r'C:\Users\admin\Projects\ResumeParser\resume_collecter'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def route_page():
    return render_template('home.html')

@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/acunor')
def acunor_page():
    return render_template('acunor.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/logout')
def logout_page():
    return render_template('login.html')

@app.route('/fetch_employee_details',methods=['GET','POST'])
def fetch_employee_details():
    data=False
    cprovider=CouchdbProvider()
    data=cprovider.retrive_data() 
    result=data.to_html()
    return render_template('fetcheroutput.html', data=result)

@app.route('/fetch_save_employee_details',methods=['GET','POST'])
def fetch_save_employee_details():
    filefetcher=FileFetcher()
    mypath=r'C:\Users\admin\Projects\ResumeParser\resume_collecter'    
    onlyfiles = [os.path.join(mypath, f) for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
    myfile=onlyfiles[0]
    print(myfile)
    filefetcher.fetch_and_parse_file(myfile)
    return render_template('datasaved.html')

@app.route('/registers', methods=['GET','POST'])
def registers():
    form = RegisterForms()    
    name=False
    password=False
    confirm=False   
    email=False
    couch=couchdb.Server('http://admin:admin@localhost:5984')
    db=couch['db_acunor']     

    if request.method=='POST':               
        if form.validate_on_submit():            
            name=form.user_name.data
            form.user_name.data=' '
            password=form.password.data
            form.password.data=' '        
            confirm=form.confirm.data
            form.password.data=' '  
            email=form.email.data
            form.email.data=' '
            
            file = request.files['file']                                                          #file saveing in folder -->start
            if file and file.filename:
                filename = secure_filename(file.filename)                                         #filename gives that uploaded name
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))                    #file saveing in folder -->     
            user={ 'loginname': name, 'password':password,'confirm':confirm,'email':email  }  
            doc=db.save(user)  
            return render_template('registernext.html', form=form)
            #return render_template('registernext.html', form=form, name=name, password=password, confirm=confirm)
    return render_template('register.html', form=form, name=name, password=password, confirm=confirm)

@app.route('/logins', methods=['GET','POST'])
def logins():
    form = LoginForms()  
    name=False
    password=False
    string =False
    row=False
    data=False    
    couch=couchdb.Server('http://admin:admin@localhost:5984')
    db=couch['db_acunor']  
    if request.method=='POST':
        if form.validate_on_submit():
            name=form.user_name.data
            form.user_name.data=' '
            password=form.password.data
            form.password.data=' '    
            rows = db.view('_all_docs', include_docs=True)            
            for row in rows:                              
                string=str(row['doc'])     
#                 data=string.split()    
#                 data=data[4:] 
                if name in string and password in string:                   
                    return render_template('loginnext.html', form=form, name=name, password=password)                       
        return render_template('logininvalid.html') 
    return render_template('login.html', form=form, name=name, password=password)

if __name__=='__main__':
    app.run()