import numpy as np
import pandas as pd
import  dataframe_image as dfi
import ansiglist

'''
[Shift Gear Thermal Damage Index 진단]
    <조건> : 시동상태
    1. Turn On 구간 탐색 > 해당 구간 내 Turn On 시간 / Current 평균 / Max Current 
    [Variable]
    'gam_ShfMotCur1',
    'gam_ShfMotCur2',
    'gbm_MotDamageIndex1',
    'gbm_MotDamageIndex2',
'''

def run(AnalySig):
    '''Data Search Start/End Index'''
    sfcon_index=[]
    sfcon_odd_start_index = AnalySig.index[(AnalySig['rbm_TTCur']==2) & (AnalySig['gam_ShfMotCur1']!=0)]
    sfcon_odd_end_index = AnalySig.index[(AnalySig['rbm_TTCur']==2) & (AnalySig['gam_ShfMotCur1']==0)]
    sfcon_even_start_index = AnalySig.index[(AnalySig['rbm_TTCur'] == 2) & (AnalySig['gam_ShfMotCur2'] != 0)]
    sfcon_even_end_index = AnalySig.index[(AnalySig['rbm_TTCur'] == 2) & (AnalySig['gam_ShfMotCur2'] == 0)]
    sfcon_index.append(sfcon_odd_start_index)
    sfcon_index.append(sfcon_even_start_index)
    sfcon_index.append(sfcon_odd_end_index)
    sfcon_index.append(sfcon_even_end_index)

    data_search_start_index = []
    All_data_search_start_index = []
    All_data_search_end_index = []
    k = 0
    while k < len(sfcon_index):  # sfcon_index 가장큰 대괄호 안의 element 개수(4개) : sfcon_odd_L/H_index, sfcon_even_L/H_index
        i = 0
        data_search_start_index = []  # odd_L/H, even_L/H 개별 Search Start_index 구한 후, 초기화 이유는 All_data_search_Start_index 변수에 그룹화 하기 위함.
        while i < len(sfcon_index[k]) - 1:  # sfcon_index를 만족하는 값 갯수
            j = 0
            while True:
                if j == 0:
                    data_search_start_index.append(sfcon_index[k][i + j])  # sfcon_index의 첫번째 데이터 저장, j=0으로 초기화 시에 Array 값 저장
                if sfcon_index[k][i + j + 1] != sfcon_index[k][i + j] + 1:  # 이후, 연속된 Array (값)을 비교하여 (값)이 연속되지 않을 경우, 해당 Array 번호 저장
                    i = i + j + 1
                    break
                else:
                    j += 1  # sfcon_index의 연속된 Array의 값이 서로 연속적일 경우 진입
                    if (i + j) == len(sfcon_index[k]) - 1:  # 언제까지 탐색할지를 결정함.(sfcon_index[k] 마지막 값까지)
                        i = i + j
                        break
        All_data_search_start_index.append(data_search_start_index)  # 하나의 list로 개별 Search_Start_index 저장
        k += 1

    All_data_search_end_index.append(All_data_search_start_index[2][1:]) #첫번째 데이터를 없애기 위함(Search end Index)
    All_data_search_end_index.append(All_data_search_start_index[3][1:])
    All_data_search_start_index=All_data_search_start_index[0:2] # 아래 반복문 수행을 위해 [2][3] Array 삭제를 위함

    print(All_data_search_start_index[0])
    print(All_data_search_end_index[0])

    ''' Odd/Even Turn On 동안 Current Mean / Current Max '''
    i=0
    odd_Analy_All =[]
    even_Analy_All =[]
    while i < len(All_data_search_start_index):
        j=0
        while j < len(All_data_search_start_index[i]):
            if i==0:
                odd_Analy_TurnOn_Time = AnalySig.iloc[All_data_search_start_index[i][j]:All_data_search_end_index[i][j]+1]['gam_ShfMotCur1'].count()*0.01
                odd_Analy_Current_Mean = AnalySig.iloc[All_data_search_start_index[i][j]:All_data_search_end_index[i][j]+1]['gam_ShfMotCur1'].mean()
                odd_Analy_Current_Max = AnalySig.iloc[All_data_search_start_index[i][j]:All_data_search_end_index[i][j]+1]['gam_ShfMotCur1'].max()
                odd_Analy_DI_diff = AnalySig.iloc[All_data_search_start_index[i][j]:All_data_search_end_index[i][j]+1]['gbm_MotDamageIndex1'].max()\
                                    - AnalySig.iloc[All_data_search_start_index[i][j]:All_data_search_end_index[i][j]+1]['gbm_MotDamageIndex1'].min()

                odd_Analy_TurnOn_Time = np.array(odd_Analy_TurnOn_Time)
                odd_Analy_Current_Mean = np.array(odd_Analy_Current_Mean)
                odd_Analy_Current_Max = np.array(odd_Analy_Current_Max)
                odd_Analy_DI_diff = np.array(odd_Analy_DI_diff)

                odd_Analy = np.append(odd_Analy_TurnOn_Time,odd_Analy_Current_Mean) #1차원배열로 결합됨 [주의] 결합할 배열은 2개만 입력가능
                odd_Analy = np.append(odd_Analy,odd_Analy_Current_Max)
                odd_Analy = np.append(odd_Analy,odd_Analy_DI_diff)

                odd_Analy_All.append(odd_Analy)
                if j == len(All_data_search_start_index[i])-1:
                    break
                j+=1

            if i==1:
                even_Analy_TurnOn_Time = AnalySig.iloc[All_data_search_start_index[i][j]:All_data_search_end_index[i][j]+1]['gam_ShfMotCur2'].count() * 0.01
                even_Analy_Current_Mean = AnalySig.iloc[All_data_search_start_index[i][j]:All_data_search_end_index[i][j]+1]['gam_ShfMotCur2'].mean()
                even_Analy_Current_Max = AnalySig.iloc[All_data_search_start_index[i][j]:All_data_search_end_index[i][j]+1]['gam_ShfMotCur2'].max()
                even_Analy_DI_diff = AnalySig.iloc[All_data_search_start_index[i][j]:All_data_search_end_index[i][j] + 1]['gbm_MotDamageIndex2'].max() \
                                    - AnalySig.iloc[All_data_search_start_index[i][j]:All_data_search_end_index[i][j] + 1]['gbm_MotDamageIndex2'].min()

                even_Analy_TurnOn_Time = np.array(even_Analy_TurnOn_Time)
                even_Analy_Current_Mean = np.array(even_Analy_Current_Mean)
                even_Analy_Current_Max = np.array(even_Analy_Current_Max)
                even_Analy_DI_diff = np.array(even_Analy_DI_diff)

                even_Analy = np.append(even_Analy_TurnOn_Time, even_Analy_Current_Mean)  # 1차원배열로 결합됨 [주의] 결합할 배열은 2개만 입력가능
                even_Analy = np.append(even_Analy, even_Analy_Current_Max)
                even_Analy = np.append(even_Analy, even_Analy_DI_diff)

                even_Analy_All.append(even_Analy)
                if j == len(All_data_search_start_index[i]) - 1:
                    break
                j+=1
        i+=1

    odd_Analy_All = pd.DataFrame(odd_Analy_All,columns=['Turn On Time','Current Mean', 'Current Max','Damage Index Diff'])
    even_Analy_All = pd.DataFrame(even_Analy_All,columns=['Turn On Time','Current Mean', 'Current Max', 'Damage Index Diff'])

    ''' Turn On 구간 중, Damage Index 증가에 영향을 준 경우만 Sorting '''
    odd_Analy_All = odd_Analy_All[odd_Analy_All['Damage Index Diff']>0]
    odd_Analy_All = odd_Analy_All.reset_index(drop=True) #상기 조건적용으로 인해 index가 순차적이지 않음. 따라서 해당 적용 / drop=true 적용하지 않으면 기존 index 보존
    even_Analy_All = even_Analy_All[even_Analy_All['Damage Index Diff']>0]
    even_Analy_All = even_Analy_All.reset_index(drop=True) #상기 조건적용으로 인해 index가 순차적이지 않음. 따라서 해당 적용 / drop=true 적용하지 않으면 기존 index 보존

    odd_DI_Diff_Interval = pd.cut(odd_Analy_All['Damage Index Diff'],[0, 0.05, 0.1, 0.2, 0.3,0.5,0.8], right=False, include_lowest=True,precision=2) # 1번인자 : 배열 / 2번인자 : 구간 / right : < A << / inclue_lowest = True 최소 값 포함 여부
    odd_Current_Mean_Interval = pd.cut(odd_Analy_All['Current Mean'],[0,3,5,7,9,11,15], right=False, include_lowest=True,precision=2) # 1번인자 : 배열 / 2번인자 : 구간 / right : < A << / inclue_lowest = True 최소 값 포함 여부
    odd_Current_Max_Interval = pd.cut(odd_Analy_All['Current Max'],[0,3,5,10,20,50], right=False, include_lowest=True,precision=2) # 1번인자 : 배열 / 2번인자 : 구간 / right : < A << / inclue_lowest = True 최소 값 포함 여부
    odd_TurnOn_Time_Interval = pd.cut(odd_Analy_All['Turn On Time'],[0,0.05,0.1,0.2,0.3,0.8], right=False, include_lowest=True,precision=2) # 1번인자 : 배열 / 2번인자 : 구간 / right : < A << / inclue_lowest = True 최소 값 포함 여부
    even_DI_Diff_Interval = pd.cut(even_Analy_All['Damage Index Diff'], [0, 0.05, 0.1, 0.2, 0.3,0.5,0.8], right=False,include_lowest=True,precision=2)  # 1번인자 : 배열 / 2번인자 : 구간 / right : < A << / inclue_lowest = True 최소 값 포함 여부
    even_Current_Mean_Interval = pd.cut(even_Analy_All['Current Mean'], [0, 3, 5, 7, 9, 11,15], right=False,include_lowest=True,precision=2)  # 1번인자 : 배열 / 2번인자 : 구간 / right : < A << / inclue_lowest = True 최소 값 포함 여부
    even_Current_Max_Interval = pd.cut(even_Analy_All['Current Max'], [0, 3, 5, 10, 20, 50], right=False,include_lowest=True,precision=2)  # 1번인자 : 배열 / 2번인자 : 구간 / right : < A << / inclue_lowest = True 최소 값 포함 여부
    even_TurnOn_Time_Interval = pd.cut(even_Analy_All['Turn On Time'], [0, 0.05, 0.1, 0.2, 0.3, 0.8], right=False,include_lowest=True,precision=2)  # 1번인자 : 배열 / 2번인자 : 구간 / right : < A << / inclue_lowest = True 최소 값 포함 여부


    odd_Max_Data =[]
    odd_Max_Data.append(odd_Analy_All['Turn On Time'].count())
    odd_Max_Data.append(odd_Analy_All['Turn On Time'].max())
    odd_Max_Data.append(odd_Analy_All['Current Mean'].max())
    odd_Max_Data.append(odd_Analy_All['Current Max'].max())
    odd_Max_Data.append(odd_Analy_All['Damage Index Diff'].max())
    odd_Max_Data.append(AnalySig['gbm_MotDamageIndex1'].max())

    even_Max_Data = []
    even_Max_Data.append(even_Analy_All['Turn On Time'].count())
    even_Max_Data.append(even_Analy_All['Turn On Time'].max())
    even_Max_Data.append(even_Analy_All['Current Mean'].max())
    even_Max_Data.append(even_Analy_All['Current Max'].max())
    even_Max_Data.append(even_Analy_All['Damage Index Diff'].max())
    even_Max_Data.append(AnalySig['gbm_MotDamageIndex2'].max())

    ''' Odd Damage Index 구간 - Current Mean(Turn On 동안) 구간 분포 '''
       # Damage Index의 의미는 전력량의 개념(시간 * 전류)
    odd_DI_Diff_Current_distribution = odd_Analy_All['Damage Index Diff'].groupby([odd_DI_Diff_Interval,odd_Current_Mean_Interval]).count()
    odd_DI_Diff_Current_distribution = odd_DI_Diff_Current_distribution.unstack(1)
    even_DI_Diff_Current_distribution = even_Analy_All['Damage Index Diff'].groupby([even_DI_Diff_Interval, even_Current_Mean_Interval]).count()
    even_DI_Diff_Current_distribution = even_DI_Diff_Current_distribution.unstack(1)

    ''' Odd Damage Index 구간 - Current Max(Turn On 동안) 구간 분포 '''
    odd_DI_Diff_Current_Max_distribution = odd_Analy_All['Damage Index Diff'].groupby([odd_DI_Diff_Interval,odd_Current_Max_Interval]).count()
    odd_DI_Diff_Current_Max_distribution = odd_DI_Diff_Current_Max_distribution.unstack(1)
    even_DI_Diff_Current_Max_distribution = even_Analy_All['Damage Index Diff'].groupby([even_DI_Diff_Interval, even_Current_Max_Interval]).count()
    even_DI_Diff_Current_Max_distribution = even_DI_Diff_Current_Max_distribution.unstack(1)

    ''' Turn On 구간 - Current Mean(Turn On 동안) 구간 분포 '''
    odd_TurnOn_Current_distribution = odd_Analy_All['Turn On Time'].groupby([odd_TurnOn_Time_Interval,odd_Current_Mean_Interval]).count()
    odd_TurnOn_Current_distribution = odd_TurnOn_Current_distribution.unstack(1)
    even_TurnOn_Current_distribution = even_Analy_All['Turn On Time'].groupby([even_TurnOn_Time_Interval, even_Current_Mean_Interval]).count()
    even_TurnOn_Current_distribution = even_TurnOn_Current_distribution.unstack(1)

    ''' Turn On Count / Max turn On Time / Max Current Mean(Turn On 구간) / Max Current / Max Damage Index Diff / Max Damage Index '''
    odd_Max_Data = pd.DataFrame(odd_Max_Data,index=['Turn On Count' ,'Max Turn On Time','Max Current Mean','Max Current','Max Damage Index Diff','Max Damage Index'])
    even_Max_Data = pd.DataFrame(even_Max_Data,index=['Turn On Count', 'Max Turn On Time', 'Max Current Mean', 'Max Current','Max Damage Index Diff', 'Max Damage Index'])

    dfi.export(odd_DI_Diff_Current_distribution,'fd_thdi11.png')
    dfi.export(odd_DI_Diff_Current_Max_distribution,'fd_thdi21.png')
    dfi.export(odd_TurnOn_Current_distribution,'fd_thdi31.png')
    dfi.export(odd_Max_Data,'fd_thdi41.png')
    dfi.export(even_DI_Diff_Current_distribution, 'fd_thdi12.png')
    dfi.export(even_DI_Diff_Current_Max_distribution, 'fd_thdi22.png')
    dfi.export(even_TurnOn_Current_distribution, 'fd_thdi32.png')
    dfi.export(even_Max_Data, 'fd_thdi42.png')


    odd_Analy_All.to_csv('odd_Analy_All.csv', index=True)
    odd_DI_Diff_Current_distribution.to_csv('odd_DI_Diff_Current_distribution.csv',index=True)
    odd_DI_Diff_Current_Max_distribution.to_csv('odd_DI_Diff_Current_Max_distribution.csv',index=True)
    odd_TurnOn_Current_distribution.to_csv('odd_TurnOn_Current_distribution.csv',index=True)
    # pd.DataFrame(AnalySig).to_csv('pd_data.csv', index=True)
    # print(odd_Analy_All)
    # print(even_Analy_All)

    ''' export excel '''
    fd_thdi_Analy = [odd_DI_Diff_Current_distribution,odd_DI_Diff_Current_Max_distribution,odd_TurnOn_Current_distribution,odd_Max_Data,
                     even_DI_Diff_Current_distribution,even_DI_Diff_Current_Max_distribution,even_TurnOn_Current_distribution,even_Max_Data]

    return(fd_thdi_Analy)
