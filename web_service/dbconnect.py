from pydoc import doc
import couchdb
import pandas as pd
import json
couch=couchdb.Server('http://admin:admin@localhost:5984')

# db=couch.create('db_acunor')


db=couch['db_acunor']


rows = db.view('_all_docs', include_docs=True)
for row in rows:
    string=str(row['doc'])
    if 'Sumu' in string:
        print('yes')


    # data=row['doc']
    # df=pd.DataFrame(data)
    # if data==name:
    #     print(df)
    

# rows = db.view('_all_docs', include_docs=True)
# data = [row['doc'] for row in rows]
# df = pd.DataFrame(data)
# print (df)

# name='chandra'
# pwd='boy'
# doc1={ 'id': 1, 'contact':{ 'loginname': name, 'password':pwd  }   }

# name='sumyu'
# pwd='girl'
# doc2={ 'id': 1,  'contact':{ 'loginname': name,   'password':pwd   }   }

# db.save(doc1)
# db.save(doc2)

