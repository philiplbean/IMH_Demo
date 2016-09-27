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
summary_2010_1 = pd.read_csv(filepath + 'DE1_0_2010_Beneficiary_Summary_File_Sample_1.csv')
summary_2010_2 = pd.read_csv(filepath + 'DE1_0_2010_Beneficiary_Summary_File_Sample_2.csv')
summary_2010 = summary_2010_1.append(summary_2010_2)
DMVstates = [11,24,51]
summary_2010 = summary_2010[summary_2010['SP_STATE_CODE'].isin(DMVstates)]
outpatient_2008_10_1 = pd.read_csv(filepath + 'DE1_0_2008_to_2010_Outpatient_Claims_Sample_1.csv')
outpatient_2008_10_2 = pd.read_csv(filepath + 'DE1_0_2008_to_2010_Outpatient_Claims_Sample_2.csv') 
outpatient_2008_10 = outpatient_2008_10_1.append(outpatient_2008_10_2)
outpatient_2008_10 = outpatient_2008_10[['DESYNPUF_ID','CLM_PMT_AMT','CLM_THRU_DT','ADMTNG_ICD9_DGNS_CD']]

#merging data 
result = pd.merge(summary_2010, outpatient_2008_10, how='inner', on=['DESYNPUF_ID'])
result = result[pd.notnull(result['ADMTNG_ICD9_DGNS_CD'])]
#result.to_csv('summary_outpatient_08-10.csv')

#zipcodes = ['207','208','210','211','212','214','217','206','222','223','209',
#           '201','220','221','200','224','225','216','205','203','227','202',
#            '204','569']

distrib = pd.read_csv(filepath + 'Data_estimates_IMH.csv')
distribZip = distrib[['Zip code first 3','Lower3','Upper3']]
distribACV = distrib[['ACV Group','Lower1','Upper1']]
distribSS = distrib[['Sponsor Service','Lower2','Upper2']]
distribHIP = distrib[['Provider Specialty HIPAA','% Encounters Lower','Upper4']]

#def meanDis(dis):
 #   dis = dis[np.isfinite(dis[[0]])]
  #  dis['mean'] = dis[[1,2]].mean(axis=1)
   # return dis
# Get distributions for Zip  
distribZip = distribZip[pd.notnull(distrib['Zip code first 3'])]
distribZip['meanZip'] = distribZip[['Lower3','Upper3']].mean(axis=1)

#Get distributions for ACV
distribACV = distribACV[pd.notnull(distrib['ACV Group'])]
distribACV['meanACV'] = distribACV[[1,2]].mean(axis=1)

#Get distributions for SS
distribSS = distribSS[pd.notnull(distrib['Sponsor Service'])]
distribSS['meanSS'] = distribSS[[1,2]].mean(axis=1)

#Get distributions for HIP
distribHIP = distribHIP[pd.notnull(distrib['Provider Specialty HIPAA'])]
distribHIP['meanHIP'] = distribHIP[[1,2]].mean(axis=1)

# distribZip = meanDis(distribZip)

def synthetic(names,probs,length):
    elements = np.array(names)
    data = np.random.choice(elements, length, probs)
    return data

result['ZIP Code'] = synthetic(distribZip['Zip code first 3'].tolist(),
                                distribZip['meanZip'].tolist(),len(result.index))

result['ACV Group'] = synthetic(distribACV['ACV Group'].tolist(),
                                distribACV['meanACV'].tolist(),len(result.index))
                                
result['Sponsor Service'] = synthetic(distribSS['Sponsor Service'].tolist(),
                                distribSS['meanSS'].tolist(),len(result.index))

result['Specialty HIPAA'] = synthetic(distribHIP['Provider Specialty HIPAA'].tolist(),
                                distribHIP['meanHIP'].tolist(),len(result.index))
