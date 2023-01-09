import numpy as np
import pandas as pd
import  dataframe_image as dfi
import ansiglist

'''
[Clutch Motor Stuck 진단]
    <진입조건> 
     1. 시동상태
     2. Clutch Target Position or Clutch Actual Position >=7mm : ccm_Clutch1TgtPosition, cam_Clutch1ActuatorPos

    <진단조건>
     1. | Clutch Target Position - Clutch Actual Position | >= 5mm : ccm_Clutch1TgtPosition, cam_Clutch1ActuatorPos
     2. | Clutch Postion Target Duty | >= 30% : cmm_c1_CltPosTgtDuty
     3. | Clutch Motor Current | >= 20A : cam_c1_CltMotCur
     
    <분석 내용>
    1. 진입조건(All) & 진단조건(1) 충족 시, 2의 분포 및 3의 분포 분석 (이유) 2,3은 1의 결과로 발생하기 때문 
'''

''' 입력 정보 '''
data_filename = 'D://시스템 응용관련//00.업무관련//01.프로젝트//6속 HEV DCT//7.검증 시험//시험데이터//고장진단 정합성 검증//210721_대아미_판교_정합성 검증.dat'
report_title = '건식 DCT GEN2 OBD2 진단 정합성 평가'
report_subtitle = 'TEST 중입니다.'
report_date = '2021-08-09'
report_department = '제어솔루션2팀'
report_filename = '2021_test.pptx'
report_info = [report_title,report_subtitle,report_date,report_department,report_filename]
''' '''

input_variable = [
    'rbm_TTCur',
    'ccm_Clutch1TgtPosition',
    'cam_Clutch1ActuatorPos',
    'cmm_c1_CltPosTgtDuty',
    'cam_c1_CltMotCur',
]

AnalySig = ansiglist.run(data_filename,input_variable)

'''
진입조건 및 Clutch Actual 값과 Target 값이 5mm 이상 차이 날 때, 
|Target Duty| 구간 및 Motor Current의 구간별 Total Control Time
'''
sfcon_odd = AnalySig[(AnalySig['rbm_TTCur']==2) &
                     ((AnalySig['ccm_Clutch1TgtPosition']>=7) | (AnalySig['cam_Clutch1ActuatorPos']>=7)) &
                     ((AnalySig['ccm_Clutch1TgtPosition']-AnalySig['cam_Clutch1ActuatorPos']).abs()>5)
]

sfcon_odd = pd.DataFrame(sfcon_odd)
sfcon_odd['abs_cmm_c1_CltPosTgtDuty'] = sfcon_odd['cmm_c1_CltPosTgtDuty'].abs()

odd_abs_ClPosTgtDuty_interval = pd.cut(sfcon_odd['abs_cmm_c1_CltPosTgtDuty'],[0,10,20,40,60,100], right=False, include_lowest=True, precision=2) # 1번인자 : 배열 / 2번인자 : 구간 / right : < A << / inclue_lowest = True 최소 값 포함 여부, 소수점의 경우,  ROUND_HALF_EVEN 방식을 사용하기 때문에 짝수에 가까운쪽으로 반올림을 함
odd_ClMotCur_interval = pd.cut(sfcon_odd['cam_c1_CltMotCur'],[0,5,10,15,20,40,80], right=False, include_lowest=True,precision=2) # 1번인자 : 배열 / 2번인자 : 구간 / right : < A << / inclue_lowest = True 최소 값 포함 여부

odd_abs_ClPosTgtDuty_ClMotCur_ControlTime = sfcon_odd['cam_c1_CltMotCur'].groupby([odd_abs_ClPosTgtDuty_interval,odd_ClMotCur_interval]).count()*0.01
odd_abs_ClPosTgtDuty_ClMotCur_ControlTime = odd_abs_ClPosTgtDuty_ClMotCur_ControlTime.unstack(1)

'''
진입조건 및 Clutch Actual 값과 Target 값이 5mm 이상 차이 날 때, ***
Turn On 구간(연속되지 않은 구간)별 Clutch Target Duty > 20% & Clutch Motor Current > 15A 충족하는 Control Time 확인 
: 두 조건은 진단 설정 값 보다 여유를 두고 조건 부여 
[Data Search 방법]
1. ***의 Index 값에서 첫번째 값을 저장하고 연속적이지 않은 Index 값 이전 값을 Search End 값으로 지정
2. 탐색된 Start / End Search Index 값에서 Clutch Targer Duty >= 20% & Clutch Motor Current >= 15A 조건을 충족하는 Control Time 계산 
'''

Odd_Data_Search_Start_index = []
Odd_Data_Search_End_index = []

i=0
while i < len(sfcon_odd.index)-1:
    if i == 0:
        Odd_Data_Search_Start_index.append(sfcon_odd.index[i])
    if sfcon_odd.index[i+1] != sfcon_odd.index[i]+1:
        Odd_Data_Search_Start_index.append(sfcon_odd.index[i+1])
        Odd_Data_Search_End_index.append(sfcon_odd.index[i])
        # print(i)
    i += 1
    if i == len(sfcon_odd.index)-1:
        Odd_Data_Search_End_index.append(sfcon_odd.index[i])


i=0
odd_Analy=[]
while i < len(Odd_Data_Search_Start_index):
        Odd_sfcon_continue_ContTime = AnalySig.iloc[Odd_Data_Search_Start_index[i]:Odd_Data_Search_End_index[i]+1]
        Odd_sfcon_continue_ContTime = Odd_sfcon_continue_ContTime[(Odd_sfcon_continue_ContTime['cmm_c1_CltPosTgtDuty'].abs()>=20) &
                                                                  (Odd_sfcon_continue_ContTime['cam_c1_CltMotCur']>=15)
        ]
        if Odd_sfcon_continue_ContTime['cam_c1_CltMotCur'].count() !=0:
            odd_Analy.append(Odd_sfcon_continue_ContTime['cam_c1_CltMotCur'].count()*0.01)
        i+=1

odd_Analy = pd.DataFrame(np.array(odd_Analy),columns=['control_time'])
odd_Analy_interval = pd.cut(odd_Analy['control_time'],[0,0.01,0.02,1], right=True, include_lowest=True,precision=2) # 1번인자 : 배열 / 2번인자 : 구간 / right : < A << / inclue_lowest = True 최소 값 포함 여부
odd_TurnOn_ControlTime = odd_Analy['control_time'].groupby([odd_Analy_interval]).count()
odd_TurnOn_ControlTime = pd.DataFrame(odd_TurnOn_ControlTime)

print(Odd_Data_Search_Start_index)
print(Odd_Data_Search_End_index)
print(odd_Analy)
print(odd_Analy_interval)

# print(np.array(odd_Analy).sum())

dfi.export(odd_abs_ClPosTgtDuty_ClMotCur_ControlTime,'fd_clmostk1.png')
dfi.export(odd_TurnOn_ControlTime,'fd_clmostk2.png')

sfcon_odd.to_csv('sfcon_odd.csv',index=True)
odd_abs_ClPosTgtDuty_ClMotCur_ControlTime.to_csv('odd_abs_ClPosTgtDuty_ClMotCur_ControlTime.csv',index=True)