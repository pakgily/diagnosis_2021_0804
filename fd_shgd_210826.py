import numpy as np
import pandas as pd
import  dataframe_image as dfi
import collections, numpy


'''
[Shift Gear Disengage Stuck 진단]
    <조건> : 시동상태
   - dmm_GBTgtGearOdd/EvenOld == g1/g2/g3/g4/g5/g6 
   - gam_ShfActFrc1/2 > | 900 or -900 | N
   - sgm_ShiftState1/2 == S_ShfBackToNSlot 
'''



def run(AnalySig):
    '''기어단별 Actuator Shift Gear Force ABS Max 값 '''
    sfcon_odd = AnalySig[(AnalySig['rbm_TTCur'] == 2) & (AnalySig['dmm_GBTgtGearOddOld'] != 'gN') & (AnalySig['sgm_ShiftState1'] == 'S_ShfBackToNSlot')]
    sfcon_even = AnalySig[(AnalySig['rbm_TTCur'] == 2) & (AnalySig['dmm_GBTgtGearEvenOld'] != 'gN') & (AnalySig['sgm_ShiftState2'] == 'S_ShfBackToNSlot')]

    def absmax (df):
        return df.abs().max()

    absmax_odd_ShfActFrc = AnalySig['gam_ShfActFrc1'].groupby(sfcon_odd['dmm_GBTgtGearOddOld']).apply(absmax)
    absmax_even_ShfActFrc = AnalySig['gam_ShfActFrc2'].groupby(sfcon_even['dmm_GBTgtGearEvenOld']).apply(absmax)

    absmax_all_gear_ShfActFrc = pd.concat([absmax_odd_ShfActFrc,absmax_even_ShfActFrc], axis=0).sort_index(axis=0)
    Analy_Table_1 = pd.DataFrame({'ShfBackToNSlot' : absmax_all_gear_ShfActFrc})
    Analy_Table_1.columns.name = 'Gear'
    print(Analy_Table_1)

    '''기어단별/Shift Gear Force 구간별 측정 시간 확인'''
    odd_ShfActFrc_interval = pd.cut(sfcon_odd['gam_ShfActFrc1'].abs(), [0, 300, 600, 900, 1200], right=True, include_lowest=True)  # 1번인자 : 배열 / 2번인자 : 구간 / right : < A << / inclue_lowest = True 최소 값 포함 여부
    odd_ActFrc_ShfState_totaltime = sfcon_odd[['dmm_GBTgtGearOddOld', 'gam_ShfActFrc1']].groupby(['dmm_GBTgtGearOddOld',odd_ShfActFrc_interval]).count() * 0.01
    odd_ActFrc_ShfState_totaltime = odd_ActFrc_ShfState_totaltime.unstack(1)
    odd_ActFrc_ShfState_totaltime = odd_ActFrc_ShfState_totaltime.rename(columns={'gam_ShfActFrc1':'ShfActFrc'})
    even_ShfActFrc_interval = pd.cut(sfcon_even['gam_ShfActFrc2'].abs(), [0, 300, 600, 900, 1200], right=True,include_lowest=True)  # 1번인자 : 배열 / 2번인자 : 구간 / right : < A << / inclue_lowest = True 최소 값 포함 여부
    even_ActFrc_ShfState_totaltime = sfcon_even[['dmm_GBTgtGearEvenOld', 'gam_ShfActFrc2']].groupby(['dmm_GBTgtGearEvenOld', even_ShfActFrc_interval]).count() * 0.01
    even_ActFrc_ShfState_totaltime = even_ActFrc_ShfState_totaltime.unstack(1)
    even_ActFrc_ShfState_totaltime = even_ActFrc_ShfState_totaltime.rename(columns={'gam_ShfActFrc2': 'ShfActFrc'})

    all_gear_ActFrc_ShfState_totaltime = pd.concat([odd_ActFrc_ShfState_totaltime, even_ActFrc_ShfState_totaltime],axis=0).sort_index(axis=0)
    Analy_Table_2 = all_gear_ActFrc_ShfState_totaltime
    print(Analy_Table_2)

    ''' 진입조건 & 고장조건 충족하는 Shift 구간 동안의 제어시간 및 분포'''
    #  Data Search Start Index
    sfcon_index=[]
    sfcon_index.append(sfcon_odd.index)
    sfcon_index.append(sfcon_even.index)

    all_data_search_start_index = []
    all_data_search_end_index = []
    i=0
    while i < len(sfcon_index):
        j=0
        data_search_start_index = []
        data_search_end_index = []
        while j < len(sfcon_index[i])-1:
            if j==0:
                data_search_start_index.append(sfcon_index[i][j])
            if sfcon_index[i][j+1] != sfcon_index[i][j]+1:
                data_search_start_index.append(sfcon_index[i][j+1])
                data_search_end_index.append(sfcon_index[i][j])
                if j + 1 == len(sfcon_index[i]) - 1:  # sfcon_index의 마지막 값이 1tic만 있을 경우
                    data_search_end_index.append(sfcon_index[i][j + 1] + 1)
                j+=1
            if j==len(sfcon_index[i])-2:
                data_search_end_index.append(sfcon_index[i][j+1]) #진입조건을 충족하는 마지막 값 저장
                j+=1
            else:
                j+=1
        i+=1
        all_data_search_start_index.append(data_search_start_index)
        all_data_search_end_index.append(data_search_end_index)

    i = 0
    odd_err_ContTime = []
    even_err_ContTime = []
    while i < len(all_data_search_start_index):
        j = 0
        while j < len(all_data_search_start_index[i]):

            if i == 0:
                sfcon_odd_Shift_interval_AbsShfFrc = AnalySig.iloc[all_data_search_start_index[i][j]:all_data_search_end_index[i][j] + 1]['gam_ShfActFrc1'].abs()
                ContTime = sfcon_odd_Shift_interval_AbsShfFrc[sfcon_odd_Shift_interval_AbsShfFrc > 900].count() #Series 불린 색인을 통한 데이터 추출
                if ContTime > 0:
                    odd_err_ContTime.append(ContTime*0.01)
                if j == len(all_data_search_start_index[i]) - 1:
                    break
                j+=1

            if i == 1:
                sfcon_even_Shift_interval_AbsShfFrc = AnalySig.iloc[all_data_search_start_index[i][j]:all_data_search_end_index[i][j] + 1]['gam_ShfActFrc2'].abs()
                ContTime = sfcon_even_Shift_interval_AbsShfFrc[sfcon_even_Shift_interval_AbsShfFrc > 900].count()  # Series 불린 색인을 통한 데이터 추출
                if ContTime > 0:
                    even_err_ContTime.append(ContTime*0.01)
                if j == len(all_data_search_start_index[i]) - 1:
                    break
                j += 1
        i+=1



    odd_err_ContTime_Analy = pd.DataFrame.from_dict([collections.Counter(odd_err_ContTime)]).T
    odd_err_ContTime_Analy.index = pd.MultiIndex.from_product([['odd'], odd_err_ContTime_Analy.index])
    even_err_ContTime_Analy = pd.DataFrame.from_dict([collections.Counter(even_err_ContTime)]).T
    even_err_ContTime_Analy.index = pd.MultiIndex.from_product([['even'], even_err_ContTime_Analy.index])

    all_err_ContTime_Analy= pd.concat([odd_err_ContTime_Analy,even_err_ContTime_Analy],axis=0)
    all_err_ContTime_Analy.rename(columns={0:'Shift Num'},inplace=True)
    all_err_ContTime_Analy.columns.name = 'control time'

    Analy_Table_3 = all_err_ContTime_Analy
    print(Analy_Table_3)

    print(odd_ActFrc_ShfState_totaltime)
    print(even_ActFrc_ShfState_totaltime)
    dfi.export(Analy_Table_1,'fd_shgd1.png')
    dfi.export(Analy_Table_2,'fd_shgd2.png')

    ''' export excel '''
    fd_shgd_Analy = [Analy_Table_1,Analy_Table_2,Analy_Table_3]


    return(fd_shgd_Analy)