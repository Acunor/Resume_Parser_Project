from flask import Flask, render_template
import pandas as pd
from IPython.display import HTML

import sys
sys.path.append(r"C:\Users\admin\Projects\ResumeParser\data_provider")
from acunor_rp_dataprovider import CouchdbProvider


from acunor_rp_filefetcher import FileFetcher

app=Flask(__name__)

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
    
    
    
if __name__=='__main__':
    app.run()