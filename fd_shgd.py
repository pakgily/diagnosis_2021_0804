import numpy as np
import pandas as pd
import  dataframe_image as dfi

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

    dfi.export(Analy_Table_1,'fd_shgd1.png')
    dfi.export(Analy_Table_2,'fd_shgd2.png')

    ''' export excel '''
    fd_shgd_Analy = [Analy_Table_1,Analy_Table_2]


    return(fd_shgd_Analy)