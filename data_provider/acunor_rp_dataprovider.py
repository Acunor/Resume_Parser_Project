import couchdb
import json
import pandas as pd

class CouchdbProvider(object):
    
    def __init__(self,url='http://admin:admin@localhost:5984'):
        self.url=url
        self.connect=self.db_connect()
        self.db=self.connect['db_test']        
        
    
    def db_connect(self):
        return couchdb.Server(self.url)
           
    
    def db_create(self):
        couch=self.db_connect()
        db=couch.create('db_test')
        return db
    
    def save_data(self,employeedetails):         
        jdata=json.dumps(employeedetails.__dict__)
        jsondata=json.loads(jdata)   
        self.db.save(jsondata)       
        
     
        
    
    def retrive_data(self):
        data=self.connect['db_test']
        rows=data.view('_all_docs',include_docs=True)
        data=[row['doc'] for row in rows]
        df=pd.DataFrame(data)
        df=df[["name","mobile","email","skills","education"]]
        df.columns = df.columns.str.upper()
        return df
#         print(type(df))
#         print(df.values.tolist())
