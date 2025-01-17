#!/usr/bin/env python
# coding: utf-8

# # Reports

# In[1]:


import os
import re
from datetime import datetime
current_datetime = datetime.now().strftime('%Y%m%d.%H%M')

import numpy as np
import pandas as pd

# for the notebook rendering 
from IPython.display import display, HTML, FileLink, Markdown
from IPython.display import FileLink as FL
from IPython.display import Markdown as MD


DIR = os.getcwd()
print(f'{DIR=}')

RDIR = os.path.join(DIR,'reports')
print(f'{RDIR=}')


# In[2]:


def break_down_buckets(idf,column,buckets,message='',nan_value=-1):
    """
    breaks a column down into buckets/bins
    """
    idf = idf.fillna(nan_value)

    print('',message,'\ncolumn: ',column, '\nbuckets: ', buckets)
    
    idf = pd.DataFrame(idf[column])
    idf['bucket'] = pd.cut(idf[column], bins=buckets)
    idf = idf.groupby(by='bucket').count()
    idf['percent'] = (idf[column]/idf[column].sum())*100
    idf['percent'] = idf['percent'].round(2)
    display(idf)

    return idf

#test
# break_down_buckets(df,'AGE_YRS',[-1,0,15,25,35,45,55,65,75,85,500])


# In[3]:


def bar(num,denom=100.0,length=30,fillchar='#',emptychar='_'):
    fillnum = ((int)( (num/denom) * length))
    return '[' + ( fillnum * fillchar ).ljust(length,emptychar)  + ']' # + f" {(num/denom)*100.0:.2f}%     " 


# In[4]:


# YYYYMMDDHHmm
DateFilter = None
DateFilter = 202501100000 # new firmware r44715
# DateFilter = 202501160000 # changed some settings in Error 404 NH


# In[5]:


def getfirmware(ssid,dt):
    if 'NH' in ssid:
        
        if dt <= 202501100810:
            return "r58881"
        elif dt > 202501100811 and dt <= 202501102101:
            return "r44715"
        elif dt > 202501102101 : #and dt <= 203000000000:
            return "r58881"
    else:
        return ""


# In[6]:


data = {}

for i in os.listdir(RDIR):
    # print(i)
    try:

        text = ''
        with open(os.path.join(RDIR, i), 'r') as f:
            text = f.read()
        # print(text)

        dt = re.findall('Datetime_alt: .*\n',text)[0]
        dt = dt.replace('Datetime_alt: ','').replace('\\n','')
        dt = int(dt)
            
        if DateFilter != None:
            if dt < DateFilter:
                #move on to next
                print('exclude',dt,DateFilter)
                continue
            else:
                print('include',dt,DateFilter)

        wifi = re.findall('^SSID:.*\n',text)[0]
        wifi = wifi.replace('\n', '').replace('SSID: ','')
        # wifi = wifi + " " + getfirmware(wifi,dt)

        pings = re.findall('.*time=.*\n',text)
        pings = [ re.sub('.*time=','',p) for p in pings]
        pings = [ re.sub('ms.*\n','',p) for p in pings]
        pings = [ int(p) for p in pings]
        # print(*pings,sep='\n')

        timeouts = re.findall('Request timed out.\n',text)

        trycount = re.findall('(Request|Reply).*\n',text)

        if wifi in data.keys():
            pass
        else:
            data[wifi] = {}
            data[wifi]['pings'] = []
            data[wifi]['timeouts'] = []
            data[wifi]['trycount'] = []
        
        data[wifi]['pings'].extend(pings)
        data[wifi]['timeouts'].extend([len(timeouts)])
        data[wifi]['trycount'].extend([len(trycount)])

    except Exception as e:
        pass
        print(i,e)

# for k in data.keys():
#     print('-'*20)
#     print(k)
#     df_pings = pd.DataFrame(data[k]['pings'])
#     print(df_pings[0].describe())
#     print()
#     print(f'Request timed out:')
#     print(f'{ sum(data[k]['timeouts']) } out of { sum(data[k]['trycount']) }')
#     print(f'{ sum(data[k]['timeouts']) / sum(data[k]['trycount']) }')

file = os.path.join(DIR,'docs','index.html')
with open(file,'w',encoding='utf8') as f:

    f.write(f'<h>{current_datetime}</h>')

    for k in data.keys():
        
        f.write('<p>' + '-'*20 + '</p>')

        f.write(f'<p>{k}</p>')
        df_pings = pd.DataFrame(data[k]['pings'])

        csvlines = df_pings.describe().to_csv()
        f.write(csvlines[4::].replace('\n','<br \>').replace(',','\t'))

        # print(df_pings)

        bdb = break_down_buckets(df_pings,0,[0,5,10,15,20,30,40,50,500])
        bdb['bar'] = bdb.percent.apply(bar)
        # display(bdb)

        f.write('<br \>')
        f.write(bdb.to_html())
        f.write('<br \>')

        f.write(f'Request timed out (failed pings):<br \>')
        f.write(f'{ sum(data[k]['timeouts']) } out of { sum(data[k]['trycount']) }<br \>')
        f.write(f'{ sum(data[k]['timeouts']) / sum(data[k]['trycount']) }')



