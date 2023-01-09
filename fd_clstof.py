import numpy as np
import pandas as pd
import  dataframe_image as dfi
import ansiglist

'''
[Clutch Stuck Off 진단]
    <진입조건> : 
     1. 시동상태
     2. | Clutch Target Position - Clutch Actual Position | < 1mm : ccm_Clutch1TgtPosition, cam_Clutch1ActuatorPos
     3. Clutch Actual Position >=10mm : cam_Clutch1ActuatorPos
     4. ssm_ClutchTgtState == SS_Drive
     5. gbm_ActGearOdd != gN
     6. iom_VSP16 <=40kph
    <진단조건> :
    1. tom_ClutchTorque_T3 < 25Nm
    2. ccm_Clutch1TgtTorque_Nm >= 100Nm
    3. dmm_Slip1 > 1000rpm     
    <분석 내용>
    1. 진입 조건(All) & 진단조건(Target Torque >=100Nm) 충족 시, 
       (1) | Act Torque - Tgt Torque | : tom_ClutchTorque_T3,ccm_Clutch1TgtTorque_Nm
       (2) | dmm_Slip1 | 
'''

''' 입력 정보 '''
data_filename = 'D://시스템 응용관련//00.업무관련//01.프로젝트//6속 HEV DCT//7.검증 시험//시험데이터//고장진단 정합성 검증//210820_장등강판로_의왕판교로.dat'
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
    'ssm_ClutchTgtState',
    'gbm_ActGearOdd',
    'iom_VSP16',
    'tom_ClutchTorque_T3',
    'ccm_Clutch1TgtTorque_Nm',
    'dmm_Slip1',
]

AnalySig = ansiglist.run(data_filename,input_variable)

sfcon_odd = AnalySig[(AnalySig['rbm_TTCur']==2) &
                     ((AnalySig['ccm_Clutch1TgtPosition']-AnalySig['cam_Clutch1ActuatorPos']).abs()<1) &
                     (AnalySig['cam_Clutch1ActuatorPos']>=10) &
                     (AnalySig['ssm_ClutchTgtState']=='SS_Drive') &
                     (AnalySig['gbm_ActGearOdd']!='gN') &
                     (AnalySig['iom_VSP16']<=40) &
                     (AnalySig['ccm_Clutch1TgtTorque_Nm']>=100)
    ]

sfcon_odd = pd.DataFrame(sfcon_odd)
sfcon_odd['abs_dmm_Slip1'] = sfcon_odd['dmm_Slip1'].abs()
sfcon_odd['odd_abs_ActTrq_TarTrq'] = (sfcon_odd['tom_ClutchTorque_T3']-sfcon_odd['ccm_Clutch1TgtTorque_Nm']).abs()

print(sfcon_odd)
odd_abs_slip_interval = pd.cut(sfcon_odd['abs_dmm_Slip1'],[0,200,600,1000,3000], right=True, include_lowest=True) # 1번인자 : 배열 / 2번인자 : 구간 / right : < A << / inclue_lowest = True 최소 값 포함 여부
odd_act_cltrq_interval = pd.cut(sfcon_odd['tom_ClutchTorque_T3'],[0,25,50,100,150,200,500], right=True, include_lowest=True) # 1번인자 : 배열 / 2번인자 : 구간 / right : < A << / inclue_lowest = True 최소 값 포함 여부
odd_abs_ActTrq_TarTrq_interval = pd.cut(sfcon_odd['odd_abs_ActTrq_TarTrq'],[0,10,20,30,100], right=True, include_lowest=True) # 1번인자 : 배열 / 2번인자 : 구간 / right : < A << / inclue_lowest = True 최소 값 포함 여부

'''진입 조건을 충족하는 경우, 
|Motor Speed - Clutch Speed] 구간별 - Actual Clutch Torque 구간별 제어시간'''
odd_AbsSlip_ActClTrq_ControlTime= sfcon_odd['dmm_Slip1'].groupby([odd_abs_slip_interval,odd_act_cltrq_interval]).count()*0.01
odd_AbsSlip_ActClTrq_ControlTime = odd_AbsSlip_ActClTrq_ControlTime.unstack(1) # 행인덱스의 0(최상위 인덱스)를 열인덱스로 바꿈
print(odd_AbsSlip_ActClTrq_ControlTime)

'''진입 조건을 충족하는 경우, 
|Actual Cluch Torque - Target Torque| 구간별 제어시간 확인
'''
odd_abs_ActTrq_TarTrq_ControlTime= sfcon_odd['odd_abs_ActTrq_TarTrq'].groupby([odd_abs_ActTrq_TarTrq_interval]).count()*0.01

'''
진입 조건을 충족하는 경우, 
Max |Motor Speed - Clutch Speed] / Max Actual Clutch Torque / Max |Actual Cluch Torque - Target Torque|
'''
odd_Max_Data = []
odd_Max_Data.append(sfcon_odd['odd_abs_ActTrq_TarTrq'].max())
odd_Max_Data.append(sfcon_odd['tom_ClutchTorque_T3'].max())
odd_Max_Data.append(sfcon_odd['odd_abs_ActTrq_TarTrq'].max())

odd_Max_Data = pd.DataFrame(odd_Max_Data, index=['Max_ABS(MoSPD - ClSPD)', 'Max Act Clutch Torque', 'Max_ABS(Act ClTrq - Tar ClTrq)'])

odd_AbsSlip_ActClTrq_ControlTime.to_csv('odd_AbsSlip_ActClTrq_ControlTime.csv', index=True)
odd_abs_ActTrq_TarTrq_ControlTime.to_csv('odd_abs_ActTrq_TarTrq_ControlTime.csv', index=True)
sfcon_odd.to_csv('sfcon_odd.csv', index=True)
