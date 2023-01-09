import numpy as np
import pandas as pd
import dataframe_image as dfi
import ansiglist
import collections, numpy

def run(Analy):
    writer = pd.ExcelWriter('210909_다이노_저온_2.xlsx', engine='xlsxwriter')
    sheet_name =['env','gri','shge','sege','shgd','gref','thdi','clstof','clmostk','clref','issno']
    i=0
    while i < len(Analy):
        j=0
        start_row = 1
        Analy_shape = [start_row]
        while j < len(Analy[i]):
            if len(Analy[i][j])!=0: #Gear Ref.와 같이 일반적인 주행 데이터로는 데이터 취득이 되지 않은 경우를 위하여 Skip을 위해
                Analy[i][j].to_excel(writer,sheet_name=sheet_name[i], startrow=start_row, startcol=0)
                Analy_shape.append(Analy[i][j].shape[0]+3)
                start_row= np.array(Analy_shape).sum()
            j+=1
        i+=1
    writer.close()
