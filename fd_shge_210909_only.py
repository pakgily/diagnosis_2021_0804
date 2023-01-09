import numpy as np
import pandas as pd
import  dataframe_image as dfi
import collections, numpy
import ansiglist

''' 입력 정보 '''
data_filename = 'D://시스템 응용관련//00.업무관련//01.프로젝트//6속 HEV DCT//7.검증 시험//시험데이터//고장진단 정합성 검증//210909_저온_engage_3,4,5,6.dat'
report_title = '건식 DCT GEN2 OBD2 진단 정합성 평가'
report_subtitle = 'TEST 중입니다.'
report_date = '2021-08-09'
report_department = '제어솔루션2팀'
report_filename = '2021_test.pptx'
report_info = [report_title,report_subtitle,report_date,report_department,report_filename]
''' '''
fd_all_Analy=[]


# input_variable= variable.add()
input_variable = [
    'rbm_TTCur',
    'gbm_GBTgtGear1',
    'gbm_GBTgtGear2',
    'gam_ShfActFrc1',
    'gam_ShfActFrc2',
    'sgm_ShiftState1',
    'sgm_ShiftState2',

]

AnalySig = ansiglist.run(data_filename,input_variable)




'''
[Shift Gear Engage Stuck 진단]
    <조건> : 시동상태 & sgm_S
   - sgm_ShiftState1/2 == S_ShfToSync or S_ShfSync or S_ShfToInGear 
   - gam_ShfActFrc1/2 > | 900 or -900 | N
   - gbm_GBTgtGear1/2 
   - gam_ShfActPos1/2
  
'''

''' 기어단/Shift State 별 Actuator Shift Gear Force ABS Max 값 '''
sfcon_odd = AnalySig[(AnalySig['rbm_TTCur'] == 2) & (AnalySig['gbm_GBTgtGear1'] != 'gN')]
sfcon_even = AnalySig[(AnalySig['rbm_TTCur'] == 2) & (AnalySig['gbm_GBTgtGear2'] != 'gN')]
# Sample Code #
# max_odd_ShfActFrc = AnalySig['gam_ShfActFrc1'].groupby([sfcon_odd['gbm_GBTgtGear1'], sfcon_odd['sgm_ShiftState1']]).max().abs()
# min_odd_ShfActFrc = AnalySig['gam_ShfActFrc1'].groupby([sfcon_odd['gbm_GBTgtGear1'], sfcon_odd['sgm_ShiftState1']]).min().abs()
# max_even_ShfActFrc = AnalySig['gam_ShfActFrc2'].groupby([sfcon_even['gbm_GBTgtGear2'], sfcon_even['sgm_ShiftState2']]).max().abs()
# min_even_ShfActFrc = AnalySig['gam_ShfActFrc2'].groupby([sfcon_even['gbm_GBTgtGear2'], sfcon_even['sgm_ShiftState2']]).min().abs()

def absmax (df):
    return df.abs().max()

absmax_odd_ShfActFrc = AnalySig['gam_ShfActFrc1'].groupby([sfcon_odd['gbm_GBTgtGear1'], sfcon_odd['sgm_ShiftState1']]).apply(absmax)
absmax_even_ShfActFrc = AnalySig['gam_ShfActFrc2'].groupby([sfcon_even['gbm_GBTgtGear2'], sfcon_even['sgm_ShiftState2']]).apply(absmax)

# [중요] 바로 위 groupby
# groupby([Series1, Series2]) :  Series1 : g1,g3,g5 / Series2 : ....

# [중요] 바로 아래 : 계층 구조를 이루는 Series 데이터 선택
# max_odd_ShfActFrc는 Series 이다. 특이하게도 계층을 이루는 Series임. 따라서 계층을 이루는 Series 데이터 선택 시, .loc[[],[]] 첫번째 [] 상위 계층, 두번째 []는 하위 계층
# max_odd_ShfActFrc.loc[:,['S_ShfToSync','S_ShfSync','S_ShfToInGear']]

# Sample Code #
# max_all_gear_ShfActFrc = pd.concat([max_odd_ShfActFrc, max_even_ShfActFrc], axis=0).sort_index(axis=0)  # 홀수/짝수 Max Synchron Speed를 (행방향)으로 붙이고 (행방향) 정렬
# min_all_gear_ShfActFrc = pd.concat([min_odd_ShfActFrc, min_even_ShfActFrc], axis=0).sort_index(axis=0)  # 홀수/짝수 Max Synchron Speed를 (행방향)으로 붙이고 (행방향) 정렬

absmax_all_gear_ShfActFrc = pd.concat([absmax_odd_ShfActFrc, absmax_even_ShfActFrc], axis=0).sort_index(axis=0)

# Sample Code #
# Analy_table_1 = pd.DataFrame({'Max': max_all_gear_ShfActFrc,'Min': min_all_gear_ShfActFrc })
# Analy_table_1 = Analy_table_1.loc[pd.IndexSlice[:,('S_ShfToSync','S_ShfSync','S_ShfToInGear')],:]
# Analy_table_1 = Analy_table_1.unstack(1)
# Analy_table_1.index.name = None
# Analy_table_1.columns.set_names('', level=1, inplace=True)

Analy_table_1 = pd.DataFrame({'ABS_MAX' : absmax_all_gear_ShfActFrc})
Analy_table_1 = Analy_table_1.loc[pd.IndexSlice[:,('S_ShfToSync','S_ShfSync','S_ShfToInGear')],:]
# [중요] 바로 위 : Multiindex를 가지는 행의 일부 데이터 선택
# df.loc[,] : ,를 기준으로 앞-행 / 뒤-열을 의미함. loc는 행 선택에 사용함.
# pd,IndexSlice[:,('S_ShfToSync','S_ShfSync','S_ShfToInGear')] : ,를 기준으로 앞은 Level 0 Index / 뒤는 level1
Analy_table_1 = Analy_table_1.unstack(1)
Analy_table_1.index.name = None
Analy_table_1.columns.set_names('Gear', level=1, inplace=True)
# Analy_table_1.columns.set_names(['',''], inplace=True)
# 바로 위와 같이 사용해도 된다.
Analy_table_1 = Analy_table_1['ABS_MAX'] #최상위 level 열 이름을 이미지에서 삭제하기 위함

'''기어단/Shift State/ Shift Gear Force 구간별 측정 시간 확인'''
odd_ShfActFrc_interval = pd.cut(sfcon_odd['gam_ShfActFrc1'].abs(),[0, 250, 500, 750, 900, 1201], right=False, include_lowest=True,precision=2)  # 1번인자 : 배열 / 2번인자 : 구간 / right : < A << / inclue_lowest = True 최소 값 포함 여부
odd_ActFrc_ShfState_totaltime = sfcon_odd[['gam_ShfActFrc1','gbm_GBTgtGear1','sgm_ShiftState1']].groupby([odd_ShfActFrc_interval,'gbm_GBTgtGear1','sgm_ShiftState1']).count() * 0.01
odd_ActFrc_ShfState_totaltime = odd_ActFrc_ShfState_totaltime.unstack(0)
odd_ActFrc_ShfState_totaltime = odd_ActFrc_ShfState_totaltime.loc[pd.IndexSlice[:,('S_ShfToSync','S_ShfSync','S_ShfToInGear')],:]
odd_ActFrc_ShfState_totaltime = odd_ActFrc_ShfState_totaltime.rename(columns={'gam_ShfActFrc1': 'ShfActFrc'})  # columns label 이름 변경 / 아래와 같이 사용해도 무방(같은 이름을 level0, level1 이 동시에 사용 시에 아래 사용이 나을 듯함)
# odd_ActFrc_ShfState_totaltime.columns.set_levels(['ShfActFrc'], level=0, inplace= True) #columns의 라벨명을 변경(name 변경이 아님)
even_ShfActFrc_interval = pd.cut(sfcon_even['gam_ShfActFrc2'].abs(), [0, 250, 500, 750, 900, 1201], right=False, include_lowest=True,precision=2)  # 1번인자 : 배열 / 2번인자 : 구간 / right : < A << / inclue_lowest = True 최소 값 포함 여부
even_ActFrc_ShfState_totaltime = sfcon_even[['gam_ShfActFrc2', 'gbm_GBTgtGear2', 'sgm_ShiftState2']].groupby([even_ShfActFrc_interval, 'gbm_GBTgtGear2', 'sgm_ShiftState2']).count() * 0.01
even_ActFrc_ShfState_totaltime = even_ActFrc_ShfState_totaltime.unstack(0)
even_ActFrc_ShfState_totaltime = even_ActFrc_ShfState_totaltime.loc[pd.IndexSlice[:, ('S_ShfToSync', 'S_ShfSync', 'S_ShfToInGear')], :]
even_ActFrc_ShfState_totaltime = even_ActFrc_ShfState_totaltime.rename(columns={'gam_ShfActFrc2': 'ShfActFrc'})  # columns label 이름 변경 / 아래와 같이 사용해도 무방(같은 이름을 level0, level1 이 동시에 사용 시에 아래 사용이 나을 듯함)
# even_ActFrc_ShfState_totaltime.columns.set_levels(['ShfActFrc'], level=0, inplace=True)
all_gear_ActFrc_ShfState_totaltime = pd.concat([odd_ActFrc_ShfState_totaltime, even_ActFrc_ShfState_totaltime],axis=0).sort_index(axis=0)  # 홀수/짝수 Max Synchron Speed를 (행방향)으로 붙이고 (행방향) 정렬
Analy_table_2 = all_gear_ActFrc_ShfState_totaltime

#naly_table_2 = odd_ActFrc_ShfState_totaltime.swaplevel(0,1,axis=0)
# [중요] 바로 위
# MultiIndex에서 Level을 바꿀 때 사용

''' 진입조건 & 고장조건 충족하는 Shift 구간 동안의 제어시간 및 분포'''
sfcon_add_odd = sfcon_odd[(sfcon_odd['sgm_ShiftState1']=='S_ShfToSync') |
                          (sfcon_odd['sgm_ShiftState1'] == 'S_ShfSync') |
                          (sfcon_odd['sgm_ShiftState1'] == 'S_ShfToInGear')
]

sfcon_add_even = sfcon_even[(sfcon_even['sgm_ShiftState2'] == 'S_ShfToSync') |
                          (sfcon_even['sgm_ShiftState2'] == 'S_ShfSync') |
                          (sfcon_even['sgm_ShiftState2'] == 'S_ShfToInGear')
                          ]

#  Data Search Start Index
sfcon_index = []
sfcon_index.append(sfcon_add_odd.index)
sfcon_index.append(sfcon_add_even.index)

all_data_search_start_index = []
all_data_search_end_index = []
i = 0
while i < len(sfcon_index):
    j = 0
    data_search_start_index = []
    data_search_end_index = []
    while j < len(sfcon_index[i]) - 1:
        if j == 0:
            data_search_start_index.append(sfcon_index[i][j])
        if sfcon_index[i][j + 1] != sfcon_index[i][j] + 1:
            data_search_start_index.append(sfcon_index[i][j + 1])
            data_search_end_index.append(sfcon_index[i][j])
            j += 1
        if j == len(sfcon_index[i]) - 2:
            data_search_end_index.append(sfcon_index[i][j + 1])  # 진입조건을 충족하는 마지막 값 저장
            j += 1
        else:
            j += 1
    i += 1
    all_data_search_start_index.append(data_search_start_index)
    all_data_search_end_index.append(data_search_end_index)

i = 0
odd_err_ContTime = []
even_err_ContTime = []
while i < len(all_data_search_start_index):
    j = 0
    while j < len(all_data_search_start_index[i]):

        if i == 0:
            sfcon_odd_Shift_interval_AbsShfFrc = \
            AnalySig.iloc[all_data_search_start_index[i][j]:all_data_search_end_index[i][j] + 1][
                'gam_ShfActFrc1'].abs()
            ContTime = sfcon_odd_Shift_interval_AbsShfFrc[
                sfcon_odd_Shift_interval_AbsShfFrc > 900].count()  # Series 불린 색인을 통한 데이터 추출
            if ContTime > 0:
                odd_err_ContTime.append(ContTime * 0.01)
            if j == len(all_data_search_start_index[i]) - 1:
                break
            j += 1

        if i == 1:
            sfcon_even_Shift_interval_AbsShfFrc = \
            AnalySig.iloc[all_data_search_start_index[i][j]:all_data_search_end_index[i][j] + 1][
                'gam_ShfActFrc2'].abs()
            ContTime = sfcon_even_Shift_interval_AbsShfFrc[
                sfcon_even_Shift_interval_AbsShfFrc > 900].count()  # Series 불린 색인을 통한 데이터 추출
            if ContTime > 0:
                even_err_ContTime.append(ContTime * 0.01)
            if j == len(all_data_search_start_index[i]) - 1:
                break
            j += 1
    i += 1

odd_err_ContTime_Analy = pd.DataFrame.from_dict([collections.Counter(odd_err_ContTime)]).T
odd_err_ContTime_Analy.index = pd.MultiIndex.from_product([['odd'], odd_err_ContTime_Analy.index])
even_err_ContTime_Analy = pd.DataFrame.from_dict([collections.Counter(even_err_ContTime)]).T
even_err_ContTime_Analy.index = pd.MultiIndex.from_product([['even'], even_err_ContTime_Analy.index])

all_err_ContTime_Analy= pd.concat([odd_err_ContTime_Analy,even_err_ContTime_Analy],axis=0)
all_err_ContTime_Analy.rename(columns={0:'Shift Num'},inplace=True)
all_err_ContTime_Analy.columns.name = 'control time'

Analy_table_3 = all_err_ContTime_Analy

odd_ActFrc_ShfState_totaltime.to_csv('210811.csv',index=True)
# odd_interval_spd_err_totaltime = odd_interval_spd_err_totaltime.unstack(0)  # 행인덱스의 0(최상위 인덱스)를 열인덱스로 바꿈
# odd_interval_spd_err_totaltime = odd_interval_spd_err_totaltime.rename(columns={'dmm_GRincorrDiff1_rpm': 'Error_Speed'})  # columns label 이름 변경 / 아래와 같이 사용해도 무방(같은 이름을 level0, level1 이 동시에 사용 시에 아래 사용이 나을 듯함)

dfi.export(Analy_table_1, 'fd_sge1.png')
dfi.export(Analy_table_2, 'fd_sge2.png')

''' export excel '''
fdi_shge_Analy = [Analy_table_1,Analy_table_2,Analy_table_3]

print(Analy_table_1)
print(Analy_table_2)
print(Analy_table_3)