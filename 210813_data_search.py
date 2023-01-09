import numpy as np
import pandas as pd
from asammdf import MDF, Signal
import  dataframe_image as dfi
import os
import time
from PIL import Image
import ansiglist
import fd_gri
import fd_shge
import reporting_t
import variable

data_filename = 'D:/MyPythonProj/210721_대아미_판교_정합성 검증.dat'
input_variable = [
    'gam_SelActPos1',
    'sgm_InitialTgtGear1',
    'gbm_GBTgtGear1',
    'sgm_CounterSolLowActive1',
    'gbm_ShiftState1',
]

AnalySig = ansiglist.run(data_filename,input_variable)
sfcon_AnalySig_index=AnalySig.index[(AnalySig['gbm_GBTgtGear1']=='g3') & (AnalySig['sgm_InitialTgtGear1']=='g3') & (AnalySig['gam_SelActPos1']>=1) & (AnalySig['gbm_ShiftState1']=='S_ShfSelLug')]
# ABC=AnalySig[(AnalySig['gbm_GBTgtGear1']=='g3') & (AnalySig['sgm_InitialTgtGear1']=='g3') & (AnalySig['gam_SelActPos1']>=1) & (AnalySig['gbm_ShiftState1']=='S_ShfSelLug')]
# ABC=ABC.tolist()

'''Data Search Start Index 추출'''
i=0
# print(ABC)
# print(type(ABC[0]+1))
data_search_start_index=[]
# print(AnalySig.index)
# print(sfcon_AnalySig_index)
#
# while i < len(sfcon_AnalySig_index)-1:
#     if sfcon_AnalySig_index[i+1]==sfcon_AnalySig_index[i]+1:
#         data_search_start_index.append(sfcon_AnalySig_index[i])
#     i+=1

# i=0
# k=0
# while i < len(sfcon_AnalySig_index)-1:
#     j=0
#     # if k==0:
#     #     data_search_start_index.append(sfcon_AnalySig_index[i])
#     while j < len(sfcon_AnalySig_index)-1:
#         if j==0:
#             data_search_start_index.append(sfcon_AnalySig_index[i+j])
#         if (i + j) == len(sfcon_AnalySig_index)-1:
#             break
#         if sfcon_AnalySig_index[i+j+1] != sfcon_AnalySig_index[i+j]+1:
#             i+=1
#             break
#         j+=1
#         # k+=1
#     i+=1

i=0
while i < len(sfcon_AnalySig_index)-1:
    j=0
    while True:
        if j==0:
            data_search_start_index.append(sfcon_AnalySig_index[i + j])
            print(i,j)
        if sfcon_AnalySig_index[i+j+1] != sfcon_AnalySig_index[i+j]+1:
            i=i+j+1
            break
        else:
            j+=1
            if (i + j) == len(sfcon_AnalySig_index) - 1:
                i=i+j
                break






print(data_search_start_index)

'''Data Search : Counter Max 추출'''
# Start Search 인덱스로 부터 4 Sample 동안 데이터를 비교하여 차이 없으면 값을 저장함.

count = AnalySig['sgm_CounterSolLowActive1'].count()
i=0
j=0
k=0
l=0
list =[]
while k < 4:
    if AnalySig['sgm_CounterSolLowActive1'][data_search_start_index[i]+j+1] == AnalySig['sgm_CounterSolLowActive1'][data_search_start_index[i]+j] :
        j+=1
        k+=1
        print('A')
        if (data_search_start_index[i]+j) == count-1:
            break
        if k == 4:
            list.append(AnalySig['sgm_CounterSolLowActive1'][data_search_start_index[i]+j])
            if i == len(data_search_start_index)-1:
                break
            i+=1
            j=0
            k=0
    else:
        j+=1
        print('B')
        if (data_search_start_index[i] + j) == count-1: #i의 경우, Array이므로 0부터 시작하기 때문에 count 시에 1을 빼야함
                # print(i)
            break





print('--------------------------')
print(list)
# print(AnalySig.loc[62684])
#






# print(ABC)


# print(AnalySig.index)
# print(AnalySig.index[AnalySig['gbm_GBTgtGear1']=='g1'])
#
# ABC=AnalySig.index[AnalySig['gbm_GBTgtGear1']=='g3']
# print(ABC[2])
# DEF=AnalySig.index[AnalySig['gbm_GBTgtGear1']=='g1'].tolist()
# print(type(DEF))
# ABC.to_csv('210815.csv',index=True)