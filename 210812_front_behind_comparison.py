import numpy as np
import pandas as pd
from asammdf import MDF, Signal
import  dataframe_image as dfi
import os
import time
from PIL import Image
import ansiglist
import fd_gri
import fd_sge
import reporting_t
import variable

data_filename = 'D:/MyPythonProj/210721_대아미_판교_정합성 검증.dat'
input_variable = [
'sgm_CounterSolLowActive1'
]

AnalySig = ansiglist.run(data_filename,input_variable)
print(AnalySig)
print(type(AnalySig))
print(AnalySig.iloc[1,0])
print(AnalySig['sgm_CounterSolLowActive1'][0])
print(type(AnalySig['sgm_CounterSolLowActive1'][0]))
print(3.3!=0)

count = AnalySig['sgm_CounterSolLowActive1'].count()

# while True:
i=0
j=0
k=0
list =[]
while j < 4:
    if AnalySig['sgm_CounterSolLowActive1'][i+1] == AnalySig['sgm_CounterSolLowActive1'][i] :
        j+=1
        i+=1
        if j == 4:
            if k==0:
                list.append(AnalySig['sgm_CounterSolLowActive1'][i])
            # if AnalySig['sgm_CounterSolLowActive1'][i] != AnalySig['sgm_CounterSolLowActive1'][i-1]:
            if AnalySig['sgm_CounterSolLowActive1'][i] != list[len(list) - 1]:
                list.append(AnalySig['sgm_CounterSolLowActive1'][i])
                # j=0
            k += 1
            j = 0
        if i == count-1: #i의 경우, Array이므로 0부터 시작하기 때문에 count 시에 1을 빼야함
                # print(i)
            break
    else :
        i+=1
        # print(i)
        if i == count-1:
            break

list = pd.Series(list)
list=list[list!=0]
print(list)
list.to_csv('210814.csv',index=True)


        # i += 1



