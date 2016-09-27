# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 12:56:31 2016

@author: philiplockwoodbean
"""

"""
Created on Mon Aug 29 15:21:09 2016
@author: walkerkehoe
"""

import pandas as pd
import numpy as np

filepath = '/Users/philiplockwoodbean/Documents/IMHDemo/'

#import CSV 
summary_2010 = pd.read_csv(filepath + 'DE1_0_2010_Beneficiary_Summary_File_Sample_1.csv')
DMVstates = [11,24,51]
summary_2010 = summary_2010[summary_2010['SP_STATE_CODE'].isin(DMVstates)]
outpatient_2008_10 = pd.read_csv(filepath + 'DE1_0_2008_to_2010_Outpatient_Claims_Sample_1.csv') 
outpatient_2008_10 = outpatient_2008_10[['DESYNPUF_ID','CLM_PMT_AMT','CLM_THRU_DT','ADMTNG_ICD9_DGNS_CD']]

distrib = pd.read_csv(filepath + 'Data_estimates_IMH.csv')
distrib = distrib[['Zip code first 3','Lower3','Upper3']]
distrib = distrib[np.isfinite(distrib['Zip code first 3'])]
distrib['meanZip'] = distrib[['Lower3','Upper3']].mean(axis=1)

#merging data 
result = pd.merge(summary_2010, outpatient_2008_10, how='inner', on=['DESYNPUF_ID'])
result = result[pd.notnull(result['ADMTNG_ICD9_DGNS_CD'])]
#result.to_csv('summary_outpatient_08-10.csv')

zipcodes = ['207','208','210','211','212','214','217','206','222','223','209',
            '201','220','221','200','224','225','216','205','203','227','202',
            '204','569']

def synthetic(names,probs,length):
    elements = np.array(names)
    data = np.random.choice(elements, length, probs)
    return data

result['zipvals'] = synthetic(distrib['Zip code first 3'].tolist(),
                                distrib['meanZip'].tolist(),len(result.index))

