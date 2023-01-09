import numpy as np
import pandas as pd
import  dataframe_image as dfi
import collections, numpy

'''
[Select Gear Engage Stuck 진단]
    <조건> : 시동상태 / <확인사항> Counter
        [Case1] Odd (H>L) : g5 > g3 : LowActiveCounter1
        [Case2] Odd (L>H) : g3 > g5 : HighActiveCounter1
        [Case3] Even (H>L) : g4 > g6 : LowActiveCounter2
        [Case3] Even (L>H) : g6 > g4 : HighActiveCounter2
        (예시) : Case1
            - sgm_InitialTgtGear1 == g3
            - gbm_GBTgtGear1 == g3
            - gbm_ShiftState1 == S_ShfSelLug
            [진단 설정 값]
            - sgm_CounterSolLowActive1 > 150 counter 
'''
def run(AnalySig):
    '''Data Search Start Index 충족 조건, 추후 HighActive 값 변경 할 것'''
    sfcon_index=[]
    sfcon_odd_L_index = AnalySig.index[(AnalySig['rbm_TTCur']==2) & (AnalySig['gbm_GBTgtGear1']=='g3') & (AnalySig['sgm_InitialTgtGear1']=='g3') & (AnalySig['gam_SelActPos1']>=1) & (AnalySig['gbm_ShiftState1']=='S_ShfSelLug')]
    sfcon_odd_H_index = AnalySig.index[(AnalySig['rbm_TTCur'] == 2) & (AnalySig['gbm_GBTgtGear1'] == 'g5') & (AnalySig['sgm_InitialTgtGear1'] == 'g5') & (AnalySig['gam_SelActPos1'] <= 6) & (AnalySig['gbm_ShiftState1'] == 'S_ShfSelLug')]
    sfcon_even_L_index = AnalySig.index[(AnalySig['rbm_TTCur'] == 2) & (AnalySig['gbm_GBTgtGear2'] == 'g6') & (AnalySig['sgm_InitialTgtGear2'] == 'g6') & (AnalySig['gam_SelActPos2'] >= 1) & (AnalySig['gbm_ShiftState2'] == 'S_ShfSelLug')]
    sfcon_even_H_index = AnalySig.index[(AnalySig['rbm_TTCur'] == 2) & (AnalySig['gbm_GBTgtGear2'] == 'g4') & (AnalySig['sgm_InitialTgtGear2'] == 'g4') & (AnalySig['gam_SelActPos2'] <= 6) & (AnalySig['gbm_ShiftState2'] == 'S_ShfSelLug')]
    sfcon_index.append(sfcon_odd_L_index)
    sfcon_index.append(sfcon_odd_H_index)
    sfcon_index.append(sfcon_even_L_index)
    sfcon_index.append(sfcon_even_H_index)

    print(len(sfcon_index))
    print(sfcon_index[0])
    print(type(sfcon_index[0]))
    print(len(sfcon_index[0]))

    # print(len(sfcon_index[k]))

    '''Data Search Start Index 충족 조건에서 첫 시작점만 추출, 추후 HighActive 값 변경 할 것
            [Search Start 시작점 추출의 의미]
            : sfcon_index 값은 기본적인 시작점을 파악하기 위해 조건을 충족하는 값을 의미한다. 
            이 때 충족하는 값에서 첫 시작점을 Search 해야함.             
            
            [Search 방법]
            sfcon_index 값의 첫번째 Array를 저장하고 다음 Array의 값이 시작 값과 비교하여 연속된 값을 가지지 않을 경우에
            해당 시점의 Array 번호와 Array의 값을 저장. 해당 Array 시점을 기준으로 다시 다음 Array 값을 비교하여 동일한 방식으로
            찾는다.
            
    '''

    data_search_start_index = []
    All_data_search_start_index =[]
    k=0
    while k < len(sfcon_index): # sfcon_index 가장큰 대괄호 안의 element 개수(4개) : sfcon_odd_L/H_index, sfcon_even_L/H_index
        i=0
        data_search_start_index = [] # odd_L/H, even_L/H 개별 Search Start_index 구한 후, 초기화 이유는 All_data_search_Start_index 변수에 그룹화 하기 위함.
        while i < len(sfcon_index[k])-1: #sfcon_index를 만족하는 값 갯수
            j=0
            while True:
                if j==0:
                    data_search_start_index.append(sfcon_index[k][i + j]) #sfcon_index의 첫번째 데이터 저장, j=0으로 초기화 시에 Array 값 저장
                    print(i,j)
                if sfcon_index[k][i+j+1] != sfcon_index[k][i+j]+1: #이후, 연속된 Array (값)을 비교하여 (값)이 연속되지 않을 경우, 해당 Array 번호 저장
                    i=i+j+1
                    break
                else:
                    j+=1 #sfcon_index의 연속된 Array의 값이 서로 연속적일 경우 진입
                    if (i + j) == len(sfcon_index[k]) - 1: #언제까지 탐색할지를 결정함.(sfcon_index[k] 마지막 값까지)
                        i=i+j
                        break
        All_data_search_start_index.append(data_search_start_index) #하나의 list로 개별 Search_Start_index 저장
        k+=1

    '''Data Search : Counter Max 추출'''
    # Start Search 인덱스로 부터 4 Sample 동안 데이터를 비교하여 차이 없으면 값을 저장함.

    count = AnalySig['sgm_CounterSolLowActive1'].count() #Active Counter 전체 데이터 수
    l=0
    active_count=[]
    all_active_count=[]

    while l < len(All_data_search_start_index): #4개
        active_count=[]
        i=0
        j=0
        k=0
        while k < 4: # 4개의 sample(40ms) 동안 값이 변하지 않을 경우 Active Counter저장하기 위한 반복
            if(l==0 or l==1): #odd_L/H에 관해 수행
                if AnalySig['sgm_CounterSolLowActive1'][All_data_search_start_index[l][i]+j+1] == AnalySig['sgm_CounterSolLowActive1'][All_data_search_start_index[l][i]+j] :
                    j+=1
                    k+=1
                    if (All_data_search_start_index[l][i]+j) == count-1: #Search 종료 시점을 정의 Active Counter 값의 마지막에서 종료
                        break
                    if k == 4:
                        active_count.append(AnalySig['sgm_CounterSolLowActive1'][All_data_search_start_index[l][i]+j]) # 4개의 sample(40ms) 동안 값이 변하지 않을 경우 Active Counter저장
                        if i == len(All_data_search_start_index[l])-1: #Search 종료 시점을 정의 Active Counter 값의 마지막에서 종료
                            break
                        i+=1
                        j=0
                        k=0
                else:
                    j+=1
                    if (All_data_search_start_index[l][i] + j) == count-1: #i의 경우, Array이므로 0부터 시작하기 때문에 count 시에 1을 빼야함, #Active Counter 변수의 인접한 데이터의 값이 같지 않을 경우
                            # print(i)
                        break

            if(l==2 or l==3):
                if AnalySig['sgm_CounterSolLowActive2'][All_data_search_start_index[l][i]+j+1] == AnalySig['sgm_CounterSolLowActive2'][All_data_search_start_index[l][i]+j] :
                    j+=1
                    k+=1
                    if (All_data_search_start_index[l][i]+j) == count-1:
                        break
                    if k == 4:
                        active_count.append(AnalySig['sgm_CounterSolLowActive2'][All_data_search_start_index[l][i]+j])
                        if i == len(All_data_search_start_index[l])-1:
                            break
                        i+=1
                        j=0
                        k=0
                else:
                    j+=1
                    if (All_data_search_start_index[l][i] + j) == count-1: #i의 경우, Array이므로 0부터 시작하기 때문에 count 시에 1을 빼야함
                            # print(i)
                        break
        all_active_count.append(active_count)
        l+=1


    print('--------------------------')
    print(all_active_count)
    print(len(all_active_count))

    '''
    Odd/Even Select Shift 방향별 Active Count Max 값 
    '''
    i=0
    all_active_count_max=[]
    while i < len(all_active_count):
        all_active_count_max.append(pd.Series(all_active_count[i]).max())
        i+=1
    all_active_count_max = pd.DataFrame(np.array(all_active_count_max),index=(['Odd_L','Odd_H','Even_L','Even_H']), columns=['Max'])
    print(all_active_count_max)

    '''
    Odd/Even Select Shift 방향별 Active Count 값과 Shift 횟수 
    '''
    i=0
    all_active_collection_counter=[]
    while i < len(all_active_count):
        all_active_collection_counter.append(collections.Counter(all_active_count[i]))
        i+=1

    print(all_active_collection_counter)
    odd_L_count_analy = pd.DataFrame.from_dict([all_active_collection_counter[0]]).T
    odd_L_count_analy.index = pd.MultiIndex.from_product([['Odd_L'],odd_L_count_analy.index])
    odd_H_count_analy = pd.DataFrame.from_dict([all_active_collection_counter[1]]).T
    odd_H_count_analy.index = pd.MultiIndex.from_product([['Odd_H'], odd_H_count_analy.index])
    even_L_count_analy = pd.DataFrame.from_dict([all_active_collection_counter[2]]).T
    even_L_count_analy.index = pd.MultiIndex.from_product([['Even_L'], even_L_count_analy.index])
    even_H_count_analy = pd.DataFrame.from_dict([all_active_collection_counter[3]]).T
    even_H_count_analy.index = pd.MultiIndex.from_product([['Even_H'], even_H_count_analy.index])

    all_active_count_analy = pd.concat([odd_L_count_analy,odd_H_count_analy,even_L_count_analy,even_H_count_analy],axis=0)
    all_active_count_analy.rename(columns={0:'Shift Num'},inplace=True)
    all_active_count_analy.columns.name = 'Active Count'
    print(all_active_count_analy)
    dfi.export(all_active_count_max, 'fd_sege1.png')
    dfi.export(all_active_count_analy,'fd_sege2.png')

    ''' export excel '''
    fd_sege_Analy = [all_active_count_max, all_active_count_analy]

    return (fd_sege_Analy)