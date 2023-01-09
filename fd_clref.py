import numpy as np
import pandas as pd
import dataframe_image as dfi
import ansiglist

'''
[Clutch Ref. Failure 진단]
    <진입조건> 
     1. 시동상태 (rbm_TTCur는 추가하지 않아도 될 듯)
     2. Clutch ref. State == 1(Ref. 시작) SET 된 시점 부터 진단 시작
       : Start Index로 사용
      
    <진단조건>
     1. Clutch Motor Current < 5A : cam_c1_CltMotCur
     2. Clutch Ref.Target Duty < =90% : cmm_Clt1RefChkTgtDuty

    <분석 내용>
    1. Clutch Ref. 시도 횟수
    2. Clutch Ref. 시, Max Clutch Motor Current : cam_c1_CltMotCur
    3. Clutch Ref. 시, Max Clutch Target Duty : cmm_Clt1RefChkTgtDuty
    4. Clutch Ref. 시, Clutch Act Position 평균 : cam_Clutch1ActuatorPos
    
    1. Data Search 
      - Start Index 추출 
        : Clutch Ref. State == 1 (Start Index 추출): cmm_c1_RefChkState 또는
          Clutch Ref. Check Target Duty = -15% 바뀌는 시점 :  cmm_Clt1RefChkTgtDuty 
      - End Index 추출
        : (1) Clutch Ref. Check Target Duty = 0% 바뀌는 시점 :  cmm_Clt1RefChkTgtDuty(정상)
          (2) Clutch Ref. Check Target Duty = -90% 바뀌는 시점 :  cmm_Clt1RefChkTgtDuty(고장)
'''

''' 입력 정보 '''
data_filename = 'D://시스템 응용관련//00.업무관련//01.프로젝트//6속 HEV DCT//7.검증 시험//시험데이터//고장진단 정합성 검증//210820_장등강판로_의왕판교로.dat'
# data_filename = 'D://시스템 응용관련//00.업무관련//01.프로젝트//6속 HEV DCT//7.검증 시험//시험데이터//고장진단 로직 검증//Clutch Reference Failure//[HEV_6DCT]_1-x_,2-2. OBD2_Clutch Reference Failure(Odd)_210521_1_보류.dat'
report_title = '건식 DCT GEN2 OBD2 진단 정합성 평가'
report_subtitle = 'TEST 중입니다.'
report_date = '2021-08-09'
report_department = '제어솔루션2팀'
report_filename = '2021_test.pptx'
report_info = [report_title, report_subtitle, report_date, report_department, report_filename]
''' '''

input_variable = [
    'rbm_TTCur',
    'cam_c1_CltMotCur',
    'cmm_Clt1RefChkTgtDuty',
    'cam_Clutch1ActuatorPos',
    'cmm_c1_RefChkState',
]

AnalySig = ansiglist.run(data_filename, input_variable)

sfcon_odd = AnalySig[(AnalySig['cmm_Clt1RefChkTgtDuty']==-15)]

Odd_Data_Search_Start_index = []
Odd_Data_Search_End_index = []


''' Start Index 추출 '''
i=0
while i < len(sfcon_odd.index)-1:
    if i == 0:
        Odd_Data_Search_Start_index.append(sfcon_odd.index[i])
    if sfcon_odd.index[i+1] != sfcon_odd.index[i]+1:
        Odd_Data_Search_Start_index.append(sfcon_odd.index[i+1])
        # print(i)
    i += 1

''' End Index 추출 '''
i=0
while i < len(Odd_Data_Search_Start_index):
    j=0
    while True :
        if AnalySig['cmm_Clt1RefChkTgtDuty'][Odd_Data_Search_Start_index[i]+j] == 0:
            Odd_Data_Search_End_index.append(Odd_Data_Search_Start_index[i]+j)
            break
        if AnalySig['cmm_Clt1RefChkTgtDuty'][Odd_Data_Search_Start_index[i]+j] == -90:
            Odd_Data_Search_End_index.append(Odd_Data_Search_Start_index[i]+j)
            break
        j+=1
        if j == len(AnalySig['cmm_Clt1RefChkTgtDuty'])-1:
            break
    i+=1

print(Odd_Data_Search_Start_index)
print(Odd_Data_Search_End_index)


''' 
데이터 분석1 : Clutch Ref. 시, Max Clutch Motor Current : cam_c1_CltMotCur 
데이터 분석2. Clutch Ref. 시, Max Clutch Target Duty : cmm_Clt1RefChkTgtDuty
데이터 분석3. Clutch Ref. 시, Clutch Act Position 평균 : cam_Clutch1ActuatorPos
'''
i=0
odd_Analy_All=[]
while i < len(Odd_Data_Search_Start_index):
    odd_Analy_1 = AnalySig['cam_c1_CltMotCur'].iloc[Odd_Data_Search_Start_index[i]:Odd_Data_Search_End_index[i]+1].max()
    odd_Analy_2 =  AnalySig['cmm_Clt1RefChkTgtDuty'].iloc[Odd_Data_Search_Start_index[i]:Odd_Data_Search_End_index[i]+1].min()
    odd_Analy_3 = AnalySig['cam_Clutch1ActuatorPos'].iloc[Odd_Data_Search_Start_index[i]:Odd_Data_Search_End_index[i]+1].mean()

    odd_Analy_1 = np.array(odd_Analy_1)
    odd_Analy_2 = np.array(odd_Analy_2)
    odd_Analy_3 = np.array(odd_Analy_3)

    odd_Analy = np.append(odd_Analy_1,odd_Analy_2)
    odd_Analy = np.append(odd_Analy,odd_Analy_3)

    odd_Analy_All.append(odd_Analy)
    i+=1

odd_cl_ref_count = len(Odd_Data_Search_Start_index)
odd_Analy_All = pd.DataFrame(odd_Analy_All,columns=['Max Current','Min Target Duty','Mean Clutch Act Pos.'])
add_data_1 = pd.DataFrame([[odd_cl_ref_count,'','']],columns=odd_Analy_All.columns,index=['Odd Clutch Ref. Count'])
odd_Analy_All = odd_Analy_All.append(add_data_1)

print(odd_cl_ref_count)
print(add_data_1)
print(odd_Analy_All)
