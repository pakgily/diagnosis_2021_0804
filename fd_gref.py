import numpy as np
import pandas as pd
import  dataframe_image as dfi
import ansiglist

'''
[Gear Ref. 진단]
    <조건> 시동상태
'''

''' 입력 정보 '''
data_filename = 'D://시스템 응용관련//00.업무관련//01.프로젝트//6속 HEV DCT//7.검증 시험//시험데이터//OBD 정책 검증//210812_Gear Ref. Inactive 천이 확인 결과_Fail.dat'
report_title = '건식 DCT GEN2 OBD2 진단 정합성 평가'
report_subtitle = 'TEST 중입니다.'
report_date = '2021-08-09'
report_department = '제어솔루션2팀'
report_filename = '2021_test.pptx'
report_info = [report_title,report_subtitle,report_date,report_department,report_filename]
''' '''

input_variable = [
    'rbm_TTCur',
    'gam_ShfActFrc1',
    'gam_ShfActFrc2',
    'gbm_rpl_State1',
    'gbm_rpl_State2',
    'gbm_rpl_ShfFullStrk_mm1',
    'gbm_rpl_ShfFullStrk_mm2',
    'gbm_rpl_StateCnt1',
    'gbm_rpl_StateCnt2',
]

AnalySig = ansiglist.run(data_filename,input_variable)

# def run(AnalySig):
'''Data Search Start Index 충족 조건 '''
sfcon_index=[]
sfcon_odd_index = AnalySig.index[(AnalySig['rbm_TTCur']==2) & (AnalySig['gbm_rpl_State1']=='RPL_SelStuckChk')]
sfcon_even_index = AnalySig.index[(AnalySig['rbm_TTCur']==2) & (AnalySig['gbm_rpl_State2']=='RPL_SelStuckChk')]
sfcon_index.append(sfcon_odd_index)
sfcon_index.append(sfcon_even_index)


'''Data Search Start Index 충족 조건에서 첫 시작점만 추출'''
   #All_data_search_start_index은 다차원 list로 [0]: odd의 Start Index의 모음 [1] : even의 Start Index의 모음

data_search_start_index = []
All_data_search_start_index = []
k = 0
while k < len(sfcon_index):  # sfcon_index 가장큰 대괄호 안의 element 개수(4개) : sfcon_odd_L/H_index, sfcon_even_L/H_index
    i = 0
    data_search_start_index = []  # odd_L/H, even_L/H 개별 Search Start_index 구한 후, 초기화 이유는 All_data_search_Start_index 변수에 그룹화 하기 위함.
    while i < len(sfcon_index[k]) - 1:  # sfcon_index를 만족하는 값 갯수
        j = 0
        while True:
            if j == 0:
                data_search_start_index.append(sfcon_index[k][i + j])  # sfcon_index의 첫번째 데이터 저장, j=0으로 초기화 시에 Array 값 저장
                print(i, j)
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


'''Data Search end Index 충족 조건에서 첫 시작점만 추출'''
i=0
j=0
All_data_search_end_index=[]
while i < len(All_data_search_start_index):
    j=0
    k=0
    data_search_end_index=[]
    while j < len(All_data_search_start_index[j]):
        if(i==0):
            if AnalySig['gbm_rpl_State1'][All_data_search_start_index[i][j]+k]=='RPL_Fail':
                data_search_end_index.append(All_data_search_start_index[i][j]+k)
                j+=1
                break
            k+=1
        if(i==1):
            if AnalySig['gbm_rpl_State2'][All_data_search_start_index[i][j]+k]=='RPL_Fail':
                data_search_end_index.append(All_data_search_start_index[i][j]+k)
                j+=1
                break
            k+=1
    All_data_search_end_index.append(data_search_end_index)
    i+=1

print(All_data_search_start_index)
print(All_data_search_end_index)

# All_data_search_start_index =[[636,676],[886,900]]
# All_data_search_end_index =[[886,900],[1129,1300]]

# AnalySig.iloc[636:886]['gbm_rpl_StateCnt1'].max()
# print(AnalySig.iloc[All_data_search_start_index[0][0]:All_data_search_end_index[0][0]][['gbm_rpl_StateCnt1','gbm_rpl_ShfFullStrk_mm1']].max())

i=0
# odd_Analy = pd.DataFrame(columns=[0,1,2,3]) #데이터프레임 선언
odd_Analy =[]
even_Analy =[]
while i < len(All_data_search_start_index):
    j=0
    print(i,j)
    while j < len(All_data_search_start_index[i]):
        if i==0:
            odd_Analy_1=AnalySig.iloc[All_data_search_start_index[i][j]:All_data_search_end_index[i][j]+1][['gbm_rpl_StateCnt1', 'gbm_rpl_ShfFullStrk_mm1', 'gam_ShfActFrc1']].max()
            odd_Analy_2 = AnalySig.iloc[All_data_search_start_index[i][j]:All_data_search_end_index[i][j]+1]['gam_ShfActFrc1'].min()
            odd_Analy_1 = np.array(odd_Analy_1)
            odd_Analy_2 = np.array(odd_Analy_2)
            odd_Analy_12 = np.append(odd_Analy_1,odd_Analy_2) #1차원배열로 결합함
            odd_Analy.append(odd_Analy_12)
            if j == len(All_data_search_start_index[j])-1:
                break
            j+=1
        if i==1:
            even_Analy_1 = AnalySig.iloc[All_data_search_start_index[i][j]:All_data_search_end_index[i][j]][
                ['gbm_rpl_StateCnt2', 'gbm_rpl_ShfFullStrk_mm2', 'gam_ShfActFrc2']].max()
            even_Analy_2 = AnalySig.iloc[All_data_search_start_index[i][j]:All_data_search_end_index[i][j]+1][
                'gam_ShfActFrc2'].min()
            even_Analy_1 = np.array(even_Analy_1)
            even_Analy_2 = np.array(even_Analy_2)
            even_Analy_12 = np.append(even_Analy_1, even_Analy_2)  # 1차원배열로 결합함
            even_Analy.append(even_Analy_12)
            if j == len(All_data_search_start_index[j]) - 1:
                break
            j += 1
    i+=1
# print(np.array(odd_Analy))
odd_Analy = pd.DataFrame(odd_Analy, columns=['Control Count[Max]','Full Stroke[Max]','ShfActFrc[Max]','ShfActFrc[Min]'])
odd_Analy.index = pd.MultiIndex.from_product([['ODD'],odd_Analy.index])
even_Analy = pd.DataFrame(even_Analy, columns=['Control Count[Max]','Full Stroke[Max]','ShfActFrc[Max]','ShfActFrc[Min]'])
even_Analy.index = pd.MultiIndex.from_product([['EVEN'],even_Analy.index])

All_Analy = odd_Analy.append(even_Analy)
print(All_Analy)
# print(odd_Analy)
# print(AnalySig.iloc[All_data_search_start_index[0]:All_data_search_start_index[0]]['gbm_rpl_StateCnt1','gbm_rpl_ShfFullStrk_mm1'])
# print(type(AnalySig.iloc[636:886]['gbm_rpl_StateCnt1'].max()))
