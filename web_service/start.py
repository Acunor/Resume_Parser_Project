# from atexit import register
# from audioop import reverse
# from pydoc import doc
# from bcrypt import os
# from click import confirm
from flask import Flask, render_template, request, flash, redirect, url_for
# from pyparsing import And
from loginform import LoginForms
from display import DisplayForms
from registerform import RegisterForms

from IPython.display import HTML

import sys
sys.path.append(r"C:\Users\admin\Projects\ResumeParser\data_provider")
from acunor_rp_dataprovider import CouchdbProvider

sys.path.append(r"C:\Users\admin\Projects\ResumeParser\controller")
from acunor_rp_filefetcher import FileFetcher

import couchdb
import pandas as pd
import json

app=Flask(__name__)

app.config['SECRET_KEY']='nerchuko'

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

@app.route('/update', methods=['GET','POST'])
def update():    
    return render_template('update.html')
               
@app.route('/fetch_employee_details',methods=['GET'])
def fetch_employee_details():
    data=False
    cprovider=CouchdbProvider()
    data=cprovider.retrive_data() 
    result=data.to_html()    
    return render_template('output.html', data=result)

@app.route('/fetch_save_employee_details',methods=['POST'])
def fetch_save_employee_details():
    filefetcher=FileFetcher()
    myfile=r'C:\Users\admin\Desktop\resumes\datascience\Dice_Resume_CV_Andrey_Uuemaa.pdf'
    filefetcher.fetch_and_parse_file(myfile)
    
    
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
                # data=string.split()    
                # details=data[4:] 
                if name in string and password in string:                   
                    return render_template('loginindex.html', form=form, name=name, password=password,string=string)                                    
        return render_template('logininvalid.html')        
                                    
        # return render_template('loginindex.html', form=form, name=name, password=password)
    return render_template('login.html', form=form, name=name, password=password)


@app.route('/registers', methods=['GET','POST'])
def registers():
    form = RegisterForms()    
    name=False
    password=False
    confirm=False   
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
            user={ 'contact':{ 'loginname': name, 'password':password,'confirm':confirm }   }  
            doc=db.save(user)                    
            return render_template('index.html', form=form, name=name, password=password, confirm=confirm)
    return render_template('register.html', form=form, name=name, password=password, confirm=confirm)
    

if __name__=='__main__':
    app.run()
