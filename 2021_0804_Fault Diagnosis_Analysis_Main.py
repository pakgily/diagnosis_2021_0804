import numpy as np
import pandas as pd
from asammdf import MDF, Signal
import  dataframe_image as dfi
import os
import time
from PIL import Image
import ansiglist
import fd_environment_210824
import fd_gri
import fd_shge_210827
import fd_sege_210826
import fd_shgd_210826
import fd_gref_210823
import fd_thdi_210823
import fd_clstof_210824
import fd_clmostk_210824
import fd_clref_210824
import fd_issno_210824
import reporting_t
import variable
import export_excel

''' 입력 정보 '''
data_filename = 'D://시스템 응용관련//00.업무관련//01.프로젝트//6속 HEV DCT//7.검증 시험//시험데이터//고장진단 정합성 검증//210909_케피코_저온시험_-30.dat'
report_title = '건식 DCT GEN2 OBD2 진단 정합성 평가'
report_subtitle = 'TEST 중입니다.'
report_date = '2021-08-09'
report_department = '제어솔루션2팀'
report_filename = '2021_test.pptx'
report_info = [report_title,report_subtitle,report_date,report_department,report_filename]
''' '''
fd_all_Analy=[]


input_variable= variable.add()
AnalySig = ansiglist.run(data_filename,input_variable)

fd_all_Analy.append(fd_environment_210824.run(AnalySig))
fd_all_Analy.append(fd_gri.run(AnalySig))
fd_all_Analy.append(fd_shge_210827.run(AnalySig))
fd_all_Analy.append(fd_sege_210826.run(AnalySig))
fd_all_Analy.append(fd_shgd_210826.run(AnalySig))
fd_all_Analy.append(fd_gref_210823.run(AnalySig)) # 일반적으로 Gear Ref.는 고장상황에서만 분석이 가능함. 따라서 excel Export 시, Skip 필요함.
fd_all_Analy.append(fd_thdi_210823.run(AnalySig))
fd_all_Analy.append(fd_clstof_210824.run(AnalySig))
fd_all_Analy.append(fd_clmostk_210824.run(AnalySig))
fd_all_Analy.append(fd_clref_210824.run(AnalySig))
fd_all_Analy.append(fd_issno_210824.run(AnalySig))

reporting_t.run(report_info)
export_excel.run(fd_all_Analy)

# B = np.array((AnalySig))
# print("--------------")
# print(type(B))
# print(B[0])
# print(B.T)
# print(pd.DataFrame(B.T))

# C = np.append(AnalySig[0].T,AnalySig[1].T, axis=1)

    # variable.insert(0,'time')
    # B=pd.Series(AnalySig,index=variable)
    # print(B)
    # print(B.loc['time'])
    # C=pd.Series.to_frame(B).T
    # print(C)
# Raw_Data = pd.DataFrame({'Time': A[0], 'dmm_GRincorrDiff1': A[4]})

# Raw_Data.to_csv('Data Visual_T.csv', index=False)
