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


template_path = os.path.join(DIR,'template.html')


# In[3]:


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


# In[4]:


def bar(num,denom=100.0,length=30,fillchar='█',emptychar='░'):
    fillnum = ((int)( (num/denom) * length))
    return '' + ( fillnum * fillchar ).ljust(length,emptychar)  + '' # + f" {(num/denom)*100.0:.2f}%     " 


# In[5]:


# YYYYMMDDHHmm
DateFilter = None
DateFilter = 202501100000 # new firmware r44715
# DateFilter = 202501160000 # changed some settings in Error 404 NH
DateFilter = 202501010000
# DateFilter = 202502021111


# In[6]:


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


# In[7]:


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


        signalstrength =  None
        try:
            signalstrength = re.findall('Signal_Strength:.*\n',text)[0]
            signalstrength = signalstrength.replace('\n', '').replace('Signal_Strength: ','').replace('%','')
        except:
            pass

        timeouts = re.findall('Request timed out.\n',text)

        trycount = re.findall('(Request|Reply).*\n',text)

        if wifi in data.keys():
            pass
        else:
            data[wifi] = {}
            data[wifi]['pings'] = []
            data[wifi]['timeouts'] = []
            data[wifi]['trycount'] = []
            data[wifi]['signalstrength'] = []
        
        data[wifi]['pings'].extend(pings)
        data[wifi]['timeouts'].extend([len(timeouts)])
        data[wifi]['trycount'].extend([len(trycount)])

        if signalstrength != None:
            data[wifi]['signalstrength'].append(int(signalstrength))

    except Exception as e:
        pass
        print(i,e)


# In[8]:


# file = os.path.join(DIR,'docs','index.html')
# with open(file,'w',encoding='utf8') as f:

#     f.write(f'<h>{current_datetime}</h>')

#     for k in data.keys():
        
#         f.write('<p>' + '-'*20 + '</p>')

#         f.write(f'<p>{k}</p>')
#         df_pings = pd.DataFrame(data[k]['pings'])

#         csvlines = df_pings.describe().to_csv()
#         f.write(csvlines[4::].replace('\n','<br \>').replace(',','\t'))

#         f.write('<br \>')
#         f.write(f'Signal Strength (min) {min(data[k]["signalstrength"])}<br \>')
#         f.write(f'Signal Strength (mean) {sum(data[k]["signalstrength"])/len(data[k]["signalstrength"]):.2f}<br \>')
#         f.write(f'Signal Strength (max) {max(data[k]["signalstrength"])}<br \>')

#         # print(df_pings)

#         bdb = break_down_buckets(df_pings,0,[0,5,10,15,20,30,40,50,500])
#         bdb['bar'] = bdb.percent.apply(bar)
#         bdb = bdb.reset_index()
        

#         # display(bdb)

#         f.write('<br \>')
#         f.write(bdb.to_html(index=False))
#         f.write('<br \>')

#         f.write(f'Request timed out (failed pings):<br \>')
#         f.write(f'{ sum(data[k]['timeouts']) } out of { sum(data[k]['trycount']) }<br \>')
#         f.write(f'{ sum(data[k]['timeouts']) / sum(data[k]['trycount']) }')


# In[9]:


segment = """
<h2 class=""><i class="nf nf-md-wifi"></i>Wifi: {%segment_header%}</h2>
<h3 class="">Signal Strength</h2>

    <div class="progress bg-dark bar-boarder" style="height: 25px;">
        <div class="progress-bar bg-dark " role="progressbar" style="width: {%zeromin%}%" aria-valuemin="0" aria-valuemax="100"></div>
        <div class="progress-bar rounded-start-2 bg-signalstrength-1 fw-semibold" role="progressbar" style="width: {%minmean%}%" aria-valuemin="0" aria-valuemax="100">{%ssmin%}%</div>
        <div class="progress-bar  bg-signalstrength-2 fw-semibold" role="progressbar" style="width: {%meanmean%}%" aria-valuemin="0" aria-valuemax="100">{%ssmean%}%</div>
        <div class="progress-bar rounded-end-2 bg-signalstrength-1 fw-semibold" role="progressbar" style="width: {%meanmax%}%" aria-valuemin="0" aria-valuemax="100">{%ssmax%}%</div>
    </div>

<br />
<h3 class="">Ping Table</h2>
{%ping_table%}

<div class="divider"></div>
"""


# In[10]:


template = ''
with open(template_path, 'r', encoding='utf8') as f:
    template = f.read()

template = template.replace('{%report_header%}',str(current_datetime))

segments = ''
for k in data.keys():
    ns = segment

    ns = ns.replace('{%segment_header%}',k)

    ssmin = min(data[k]["signalstrength"])
    ssmean = sum(data[k]["signalstrength"])/len(data[k]["signalstrength"])
    ssmax = max(data[k]["signalstrength"])

    ns = ns.replace('{%zeromin%}',f'{ssmin:.2f}')
    ns = ns.replace('{%minmean%}',f'{ssmean-ssmin-2:.2f}')
    ns = ns.replace('{%meanmean%}',f'{4:.2f}')
    ns = ns.replace('{%meanmax%}',f'{ssmax-ssmean-2:.2f}')

    ns = ns.replace('{%ssmin%}',f'{ssmin:.0f}')
    ns = ns.replace('{%ssmean%}',f'{ssmean:.0f}')
    ns = ns.replace('{%ssmax%}',f'{ssmax:.0f}')

    df_pings = pd.DataFrame(data[k]['pings'])
    bdb = break_down_buckets(df_pings,0,[0,5,10,15,20,30,40,50,500])
    bdb['bar'] = bdb.percent.apply(bar)
    bdb = bdb.reset_index()

    # ns = ns.replace('{%ping_table%}',bdb.to_html(index=False,justify='left'))
    # ns = ns.replace('\"dataframe\"','\"table table-dark table-striped\"')

    failed_pings = sum(data[k]['timeouts'])
    failed_percent = f"{failed_pings/sum(data[k]['trycount']):.0f}"

    tbl = ''
    tbl += '<table class="table table-dark table-stripedx">\n'
    tbl += """
    <thead>
        <tr style="text-align: left;">
        <th>bucket</th>
        <th></th>
        </tr>
    </thead>
    <tbody>
    """
    for i,row in bdb.iterrows():
        print(i)
        # bucket = row['bucket']
        bucket = re.sub(r'[\(\]]', '', str(row['bucket']))
        bucket = re.sub(r',', '-', bucket)
        bucket = re.sub(r' ', '', bucket)
        tbl += f"""
            <tr>
            <td class="col-1">{bucket}</td>
            <td class="col-12">
                <div class="progress bar-boarder bg-dark">
                <div class="progress-bar overflow-visible bar-ping rounded" style="width: {row['percent']}%; height:25px">
                    <span class="badge text-start">
                    {row[0]} | {row['percent']}%
                    </span>
                </div>
                </div>
            </td>
            </tr>
        """
    tbl += f"""
        <tr>
        <td class="col-1 text-danger">Failed</td>
        <td class="col-12">
            <div class="progress bar-boarder-danger bg-dark">
            <div class="progress-bar overflow-visible bg-danger  rounded" style="width: {failed_percent}%; height:25px">
                <span class="badge-failed text-start">
                {failed_pings} | {failed_percent}%
                </span>
            </div>
            </div>
        </td>
        </tr>
    """
    tbl += """
    </table>
    </tbody>
    """

    ns = ns.replace('{%ping_table%}',tbl)

    segments += ns

template = template.replace('{%segments%}',segments)

file = os.path.join(DIR,'docs','index.html')
with open(file,'w',encoding='utf8') as f:
    f.write(template)

