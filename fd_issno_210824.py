import numpy as np
import pandas as pd
import dataframe_image as dfi
import ansiglist

'''
[Input Speed No Pulse 진단]
    <진입조건> 
    1. rbm_TTCur == 2 & 
    2. iom_VSP16 >= 20 &
    3. gbm_ActGearOdd != gN
    4. dmm_WhlSpdErr_flg == 0(No Error)
    
    <진단조건>
    1. Ni1spd_IssNP <= 0rpm

    <분석 내용>
    1. 진입조건 & 진단조건 충족하는 Total Control Time
    2. 진입조건 & 진단조건(No Pulse) 지속 시간 분포

'''

def run(AnalySig):
    '''
    데이터 분석1 :
       1. 진입/진단 조건 충족하는 Control Time
       2. 진입 조건 충족하는 Control Time
        '''
    sfcon_odd = AnalySig[(AnalySig['rbm_TTCur']==2) &
                         (AnalySig['iom_VSP16']>=20) &
                         (AnalySig['gbm_ActGearOdd']!='gN') &
                         (AnalySig['dmm_WhlSpdErr_flg']=='OFF')
    ]

    sfcon_even = AnalySig[(AnalySig['rbm_TTCur']==2) &
                         (AnalySig['iom_VSP16']>=20) &
                         (AnalySig['gbm_ActGearEven']!='gN') &
                         (AnalySig['dmm_WhlSpdErr_flg']=='OFF')
    ]

    sfcon_err_odd = AnalySig[(AnalySig['rbm_TTCur']==2) &
                         (AnalySig['iom_VSP16']>=20) &
                         (AnalySig['gbm_ActGearOdd']!='gN') &
                         (AnalySig['dmm_WhlSpdErr_flg']=='OFF') &
                         (AnalySig['Ni1spd_IssNP']<=0)
    ]

    sfcon_err_even = AnalySig[(AnalySig['rbm_TTCur']==2) &
                         (AnalySig['iom_VSP16']>=20) &
                         (AnalySig['gbm_ActGearEven']!='gN') &
                         (AnalySig['dmm_WhlSpdErr_flg']=='OFF') &
                         (AnalySig['Ni2spd_IssNP']<=0)
    ]

    sfcon_odd_total = len(sfcon_odd)*0.01
    sfcon_even_total = len(sfcon_even)*0.01

    sfcon_err_odd_total_ContTime = len(sfcon_err_odd)*0.01
    sfcon_err_even_total_ContTime = len(sfcon_err_even)*0.01

    Analy_1= pd.DataFrame([[sfcon_odd_total,sfcon_err_odd_total_ContTime],[sfcon_even_total,sfcon_err_even_total_ContTime]],
                 index=['Odd','Even'], columns=['sfcon_total_ContTime','sfcon_err_total_ContTime'])

    print(sfcon_odd_total)
    print(sfcon_even_total)
    print(sfcon_err_odd_total_ContTime)
    print(sfcon_err_even_total_ContTime)

    '''
    진입조건 & 진단조건(No Pulse) 지속 시간 분포
    '''

    ''' Start/End Index Searching'''
    Odd_Data_Search_Start_index = []
    Odd_Data_Search_End_index = []
    Even_Data_Search_Start_index = []
    Even_Data_Search_End_index = []

    i=0
    while i < len(sfcon_err_odd.index)-1:
        if i == 0:
            Odd_Data_Search_Start_index.append(sfcon_err_odd.index[i])
        if sfcon_err_odd.index[i+1] != sfcon_err_odd.index[i]+1:
            Odd_Data_Search_Start_index.append(sfcon_err_odd.index[i+1])
            Odd_Data_Search_End_index.append(sfcon_err_odd.index[i])
            # print(i)
        i += 1
        if i == len(sfcon_err_odd.index)-1:
            Odd_Data_Search_End_index.append(sfcon_err_odd.index[i])



    i=0
    while i < len(sfcon_err_even.index)-1:
        if i == 0:
            Even_Data_Search_Start_index.append(sfcon_err_even.index[i])
        if sfcon_err_even.index[i+1] != sfcon_err_even.index[i]+1:
            Even_Data_Search_Start_index.append(sfcon_err_even.index[i+1])
            Even_Data_Search_End_index.append(sfcon_err_even.index[i])
            # print(i)
        i += 1
        if i == len(sfcon_err_even.index)-1:
            Even_Data_Search_Start_index.append(sfcon_err_even.index[i])

    print(Odd_Data_Search_Start_index)
    print(Odd_Data_Search_End_index)

    print(Even_Data_Search_Start_index)
    print(Even_Data_Search_End_index)



    '''진입조건 & 진단조건 충족 지속 Control Time'''
    Odd_Continue_ContTime = []
    Even_Continue_ContTime = []
    i=0
    while i < len(Odd_Data_Search_Start_index):
            odd_Analy_1= AnalySig['Ni1spd_IssNP'].iloc[Odd_Data_Search_Start_index[i]:Odd_Data_Search_End_index[i]+1].count()
            Odd_Continue_ContTime.append(odd_Analy_1)
            i+=1

    i=0
    while i < len(Even_Data_Search_Start_index):
            even_Analy_1= AnalySig['Ni2spd_IssNP'].iloc[Even_Data_Search_Start_index[i]:Even_Data_Search_End_index[i]+1].count()
            Even_Continue_ContTime.append(even_Analy_1)
            i+=1

    All_Continue_ContTime = pd.DataFrame([Odd_Continue_ContTime,Even_Continue_ContTime],index=['Odd_Continue_ContTime','Even_Continue_ContTime'])
    Analy_2 = All_Continue_ContTime.T

    print(Analy_1)
    print(Analy_2)


    ''' export excel '''
    fd_issno_Analy = [Analy_1, Analy_2]

    return(fd_issno_Analy)