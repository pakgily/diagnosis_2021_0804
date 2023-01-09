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


def run(AnalySig):
    '''
    진입조건 및 Clutch Actual 값과 Target 값이 5mm 이상 차이 날 때,
    |Target Duty| 구간 및 Motor Current의 구간별 Total Control Time
    '''
    sfcon_odd = AnalySig[(AnalySig['rbm_TTCur']==2) &
                         ((AnalySig['ccm_Clutch1TgtPosition']>=7) | (AnalySig['cam_Clutch1ActuatorPos']>=7)) &
                         ((AnalySig['ccm_Clutch1TgtPosition']-AnalySig['cam_Clutch1ActuatorPos']).abs()>5)
    ]

    sfcon_even = AnalySig[(AnalySig['rbm_TTCur']==2) &
                         ((AnalySig['ccm_Clutch2TgtPosition']>=7) | (AnalySig['cam_Clutch2ActuatorPos']>=7)) &
                         ((AnalySig['ccm_Clutch2TgtPosition']-AnalySig['cam_Clutch2ActuatorPos']).abs()>5)
    ]

    sfcon_odd = pd.DataFrame(sfcon_odd)
    sfcon_even = pd.DataFrame(sfcon_even)
    sfcon_odd['abs_cmm_c1_CltPosTgtDuty'] = sfcon_odd['cmm_c1_CltPosTgtDuty'].abs()
    sfcon_even['abs_cmm_c2_CltPosTgtDuty'] = sfcon_even['cmm_c2_CltPosTgtDuty'].abs()

    odd_abs_ClPosTgtDuty_interval = pd.cut(sfcon_odd['abs_cmm_c1_CltPosTgtDuty'],[0,10,20,30,50,70,100], right=False, include_lowest=True, precision=2) # 1번인자 : 배열 / 2번인자 : 구간 / right : < A << / inclue_lowest = True 최소 값 포함 여부, 소수점의 경우,  ROUND_HALF_EVEN 방식을 사용하기 때문에 짝수에 가까운쪽으로 반올림을 함
    odd_ClMotCur_interval = pd.cut(sfcon_odd['cam_c1_CltMotCur'],[0,5,10,15,20,40,80], right=False, include_lowest=True,precision=2) # 1번인자 : 배열 / 2번인자 : 구간 / right : < A << / inclue_lowest = True 최소 값 포함 여부
    even_abs_ClPosTgtDuty_interval = pd.cut(sfcon_even['abs_cmm_c2_CltPosTgtDuty'],[0,10,20,30,50,70,100], right=False, include_lowest=True, precision=2) # 1번인자 : 배열 / 2번인자 : 구간 / right : < A << / inclue_lowest = True 최소 값 포함 여부, 소수점의 경우,  ROUND_HALF_EVEN 방식을 사용하기 때문에 짝수에 가까운쪽으로 반올림을 함
    even_ClMotCur_interval = pd.cut(sfcon_even['cam_c2_CltMotCur'],[0,5,10,15,20,40,80], right=False, include_lowest=True,precision=2) # 1번인자 : 배열 / 2번인자 : 구간 / right : < A << / inclue_lowest = True 최소 값 포함 여부

    odd_abs_ClPosTgtDuty_ClMotCur_ControlTime = sfcon_odd['cam_c1_CltMotCur'].groupby([odd_abs_ClPosTgtDuty_interval,odd_ClMotCur_interval]).count()*0.01
    odd_abs_ClPosTgtDuty_ClMotCur_ControlTime = odd_abs_ClPosTgtDuty_ClMotCur_ControlTime.unstack(1)
    odd_abs_ClPosTgtDuty_ClMotCur_ControlTime.index = pd.MultiIndex.from_product([['Odd'], odd_abs_ClPosTgtDuty_ClMotCur_ControlTime.index])
    odd_abs_ClPosTgtDuty_Max = sfcon_odd['abs_cmm_c1_CltPosTgtDuty'].max()
    odd_ClMotCur_Max = sfcon_odd['cam_c1_CltMotCur'].max()

    even_abs_ClPosTgtDuty_ClMotCur_ControlTime = sfcon_even['cam_c2_CltMotCur'].groupby([even_abs_ClPosTgtDuty_interval,even_ClMotCur_interval]).count()*0.01
    even_abs_ClPosTgtDuty_ClMotCur_ControlTime = even_abs_ClPosTgtDuty_ClMotCur_ControlTime.unstack(1)
    even_abs_ClPosTgtDuty_ClMotCur_ControlTime.index = pd.MultiIndex.from_product([['Even'], even_abs_ClPosTgtDuty_ClMotCur_ControlTime.index])
    even_abs_ClPosTgtDuty_Max = sfcon_even['abs_cmm_c2_CltPosTgtDuty'].max()
    even_ClMotCur_Max = sfcon_even['cam_c2_CltMotCur'].max()

    all_abs_ClPosTgtDuty_ClMotCur_ControlTime = pd.concat([odd_abs_ClPosTgtDuty_ClMotCur_ControlTime, even_abs_ClPosTgtDuty_ClMotCur_ControlTime])
    all_Max_Data =pd.DataFrame([odd_abs_ClPosTgtDuty_Max,odd_ClMotCur_Max,even_abs_ClPosTgtDuty_Max,even_ClMotCur_Max],
                               index=['odd_abs_ClPosTgtDuty_Max','odd_ClMotCur_Max','even_abs_ClPosTgtDuty_Max','even_ClMotCur_Max'])

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
    Even_Data_Search_Start_index = []
    Even_Data_Search_End_index = []

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

    i = 0
    while i < len(sfcon_even.index) - 1:
        if i == 0:
            Even_Data_Search_Start_index.append(sfcon_even.index[i])
        if sfcon_even.index[i + 1] != sfcon_even.index[i] + 1:
            Even_Data_Search_Start_index.append(sfcon_even.index[i + 1])
            Even_Data_Search_End_index.append(sfcon_even.index[i])
            # print(i)
        i += 1
        if i == len(sfcon_even.index) - 1:
            Even_Data_Search_End_index.append(sfcon_even.index[i])

    i = 0
    even_Analy = []
    while i < len(Even_Data_Search_Start_index):
        Even_sfcon_continue_ContTime = AnalySig.iloc[Even_Data_Search_Start_index[i]:Even_Data_Search_End_index[i] + 1]
        Even_sfcon_continue_ContTime = Even_sfcon_continue_ContTime[
            (Even_sfcon_continue_ContTime['cmm_c2_CltPosTgtDuty'].abs() >= 20) &
            (Even_sfcon_continue_ContTime['cam_c2_CltMotCur'] >= 15)
            ]
        if Even_sfcon_continue_ContTime['cam_c2_CltMotCur'].count() != 0:
            even_Analy.append(Even_sfcon_continue_ContTime['cam_c2_CltMotCur'].count() * 0.01)
        i += 1

    odd_Analy = pd.DataFrame(np.array(odd_Analy),columns=['control_time'])
    odd_Analy_interval = pd.cut(odd_Analy['control_time'],[0,0.01,0.02,1], right=True, include_lowest=True,precision=2) # 1번인자 : 배열 / 2번인자 : 구간 / right : < A << / inclue_lowest = True 최소 값 포함 여부
    odd_TurnOn_ControlTime = odd_Analy['control_time'].groupby([odd_Analy_interval]).count()
    odd_TurnOn_ControlTime = pd.DataFrame(odd_TurnOn_ControlTime)
    odd_TurnOn_ControlTime.index = pd.MultiIndex.from_product([['Odd'], odd_TurnOn_ControlTime.index])

    odd_TurnOn_Max_ControlTime = odd_Analy['control_time'].max()

    even_Analy = pd.DataFrame(np.array(even_Analy), columns=['control_time'])
    even_Analy_interval = pd.cut(even_Analy['control_time'], [0, 0.01, 0.02, 1], right=True, include_lowest=True,precision=2)  # 1번인자 : 배열 / 2번인자 : 구간 / right : < A << / inclue_lowest = True 최소 값 포함 여부
    even_TurnOn_ControlTime = even_Analy['control_time'].groupby([even_Analy_interval]).count()
    even_TurnOn_ControlTime = pd.DataFrame(even_TurnOn_ControlTime)
    even_TurnOn_ControlTime.index = pd.MultiIndex.from_product([['Even'], even_TurnOn_ControlTime.index])

    even_TurnOn_Max_ControlTime = even_Analy['control_time'].max()

    all_TurnOn_ControlTime = pd.concat([odd_TurnOn_ControlTime,even_TurnOn_ControlTime])
    all_TurnOn_ControlTime = all_TurnOn_ControlTime.unstack(1).sort_index(axis=0, level=0, ascending=False)
    all_TurnOn_Max_ControlTime = pd.DataFrame([odd_TurnOn_Max_ControlTime,even_TurnOn_Max_ControlTime],
                                              index = ['odd_TurnOn_Max_ControlTime','even_TurnOn_Max_ControlTime'])


    ''' export excel '''
    fd_clmostk_Analy = [all_abs_ClPosTgtDuty_ClMotCur_ControlTime, all_Max_Data, all_TurnOn_ControlTime, all_TurnOn_Max_ControlTime]

    return(fd_clmostk_Analy)
