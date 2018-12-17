
# coding: utf-8

# In[401]:


import facebook
from prettytable import PrettyTable
from collections import Counter
import json
from operator import itemgetter
import matplotlib.pyplot as plt
import numpy as np
from pandas.io.json import json_normalize
from html.parser import HTMLParser
import string
import requests
import random
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import jaccard_similarity_score


# In[402]:


#CONNECT TO FACEBOOK GRAPH API USING THE OAUTH TOKEN AND COLLECT EVENTS
from json import dumps, loads

ACCESS_TOKEN = 'EAAdKoWwnlicBAIvlV2K9b5WM9UFKEk2ks1wJgjbYvzqp5ifz1fZCKy0Kciar0ZAd61k0iC8iaqtver24naZB8NcBBmRKjWZCketapJImXxzRZAn043isj1r7P1l15BZCLFEbeWlPOxRZB16WIWjYzDTygvF4Ov8IOIZD'
g = facebook.GraphAPI(ACCESS_TOKEN, version=2.7)

def geteventfor(topic):
    link = string.Template("""/search?q=$topic&type=event&limit=10000""").substitute({"topic":topic})
    print (link)
    events = g.request(link) #Poetry, Sports, Music 
    eList = list()
    while(True):
        try:
            for event in events['data']:
                eventid = event['id']
                eList.append(loads((dumps(g.get_object(id=eventid,
                fields='name,attending_count,category,declined_count,description,\
                end_time,interested_count,is_canceled,is_page_owned,maybe_count,\
                noreply_count,owner,parent_group,place,ticket_uri,timezone,type,updated_time')))))
            # Attempt to make a request to the next page of data, if it exists.
            events=requests.get(events['paging']['next']).json()
        except KeyError:
            break
        except Exception as e:
            print (e)
            break
    return json_normalize(eList)


# In[403]:


df= geteventfor('Sports')


# In[404]:


#df=df_sports[['id','category','name','attending_count','ticket_uri','description']]

df


# In[405]:


#import os
#os.path.abspath('/Users/sharonsubathran/Desktop/')
#df.to_csv(os.path.abspath('/Users/sharonsubathran/Desktop/sports'), sep=',')


# In[406]:


usr1 = []
usr2 = []
usr3 = []
usr4 = []
usr5 = []
usr6 = []
usr7 = []
usr8 = []
usr9 = []
usr10 = []
usr11 = []
usr12 = []
usr13 = []
usr14 = []
usr15 = []


# In[407]:


for x in range(len(df_poetry)):
    usr1.append(random.randint(0,1))
    
for x in range(len(df_music)):
    usr2.append(random.randint(0,1))
    
for x in range(len(df)):
    usr3.append(random.randint(0,1))
    
for x in range(len(df_poetry)):
    usr4.append(random.randint(0,1))
    #print (usr)
    
for x in range(len(df_music)):
    usr5.append(random.randint(0,1))
    
for x in range(len(df)):
    usr6.append(random.randint(0,1))
    
for x in range(len(df_poetry)):
    usr7.append(random.randint(0,1))
    #print (usr)
    
for x in range(len(df_music)):
    usr8.append(random.randint(0,1))
    
for x in range(len(df)):
    usr9.append(random.randint(0,1))
    
for x in range(len(df_poetry)):
    usr10.append(random.randint(0,1))
    #print (usr)
    
for x in range(len(df_music)):
    usr11.append(random.randint(0,1))
    
for x in range(len(df)):
    usr12.append(random.randint(0,1))
    
for x in range(len(df_poetry)):
    usr13.append(random.randint(0,1))
    #print (usr)
    
for x in range(len(df_music)):
    usr14.append(random.randint(0,1))
    
for x in range(len(df)):
    usr15.append(random.randint(0,1))


# In[408]:


len(df)


# In[409]:



df['User_1'] = usr3


df['User_2'] = usr6


df['User_3'] = usr9


df['User_4'] = usr12


df['User_5'] = usr15


# In[410]:


df_s = df[['name','category','User_1', 'User_2','User_3', 'User_4','User_5']]


# In[411]:


df_s


# In[412]:


s = df_p['User_5'].sum()
s


# In[413]:


df_st = df_s.T

df_st.columns = df_st.iloc[0]
df_st = df_st[1:]


# In[414]:


userlist = ['User_'+str(x) for x in range(1,6)]
print(userlist)


# In[415]:


#Calculate the similarity between users in the list
def siml(df):
    a = []
    for mainuser in range(1,6):
        USER1 = dict()
        for u in range(1,6):
            if mainuser != u:
                USER1[u] = jaccard_similarity_score(df['User_'+str(mainuser)], df['User_'+str(u)])

        print(USER1)
        a.append(USER1)

    A = pd.DataFrame(a)
    A = A.rename(index={0: 'User_1', 1: 'User_2', 2: 'User_3', 3: 'User_4', 4: 'User_5'})   
    A = A.rename(columns={1 : 'User_1', 2 : "User_2", 3 : "User_3", 4 : "User_4", 5 : "User_5"})
    A = A.fillna(0)
    return (A)
    


# In[416]:


S = siml(df_s)
S
df_s = df_s.dropna(axis = 0, how='any')
CE = CE.dropna(axis=0, how='any')


# In[417]:


#Recommendations for each user in the list   
for i in userlist:
    sm = S[str(i)].idxmax()
    print ("\n", i,"is most like", sm, "\n")
    CE = currentEvents(i)
    SE = recommend(i,sm)
    print ("'Current Event' :{'Category':",CE['category'].iloc[1] , "'Event Name':",CE['name'].iloc[1] ,"},\n Recommendation:[{'Category': ",SE['category'].iloc[1] ,"'Event name:'", SE['name'].iloc[1] ,"},{'Category': ",SE['category'].iloc[2] ,"'Event name:'", SE['name'].iloc[2] ,"}}]",)
   
    #,'Event Name':,CE[name]},'Recommendation: {'Category':' SE[Category], 'Relevance': rel, 'Event Name': SE[name]}), 


# In[418]:


#SEND A USER TO THIS FUNCTION TO GET THEIR CURRENT RECOMMENDATIONS
def currentEvents(user): 
    return df_s[df_s[user]==1]


# In[419]:


#SEND TWO USERS TO THIS FUNCTION, RECOMMEND EVENTS FROM THE SECOND USER'S EVENT LIST WHICH THE FIRST ONE HASNT BEEN TO
def recommend(recommendTo,recommendFrom): #Usage:- recommend('User_1','User_3') --- RecommendTo='User_1', RecommendFrom='User_3'
    return df_s[(df_s[recommendTo]==0) & (df_s[recommendFrom])][['name','category']]


# In[420]:


print(jaccard_similarity_score(df_p['User_1'], df_p['User_4']))


# In[380]:


print (df_s.shape)

