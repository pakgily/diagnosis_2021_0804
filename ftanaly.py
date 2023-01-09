from asammdf import MDF, Signal
import numpy as np
import pandas as pd
import  dataframe_image as dfi
import os
import time
from PIL import Image


''' 계측 데이터(MDF) 샘플 Sig. Decode 및 가공 '''
with MDF('D:/MyPythonProj/210721_대아미_판교_정합성 검증.dat', version='3.30') as mdf_file :
    mdf_file_Resample = mdf_file.resample(0.01)
    # Rbm_TTCur(2) 시점만 분석하도록 변경
    sample_time = mdf_file_Resample.get('dmm_GRincorrDiff1_rpm').timestamps
    sig1 = mdf_file_Resample.get('dmm_GRincorrDiff1_rpm').samples
    sig2 = mdf_file_Resample.get('dmm_GRincorrDiff2_rpm').samples
    sig3 = mdf_file_Resample.get('gbm_ActGearOdd').samples
    sig4 = mdf_file_Resample.get('gbm_ActGearEven').samples
    sig5 = mdf_file_Resample.get('iom_VSP16').samples
    sig6 = mdf_file_Resample.get('rbm_TTCur').samples
    ''' '''

    print(type(sig1))
    print(type(sig1[0]))
    print(type(sig3[0]))
    '''type(Byte) Decode'''
    sig3_Conv = list()
    sig4_Conv = list()
    data_num = len(sig1)
    j = 0
    while j < data_num :
        sig3_Conv.append(sig3[j].decode('utf-8'))
        sig4_Conv.append(sig4[j].decode('utf-8'))
        j+=1
    ''' '''
    print(type(sig3_Conv[0]))

    Raw_Data = pd.DataFrame({'Time': sample_time, 'dmm_GRincorrDiff1': sig1, 'dmm_GRincorrDiff2': sig2, 'gbm_ActGearOdd': sig3_Conv, 'gbm_ActGearEven': sig4_Conv, 'ABS_dmm_GRincorrDiff1': np.abs(sig1), 'ABS_dmm_GRincorrDiff2': np.abs(sig2), 'iom_VSP16': sig5,'rbm_TTCur': sig6})
    Odd_Data = Raw_Data[(Raw_Data['rbm_TTCur'] == 2) & (Raw_Data['gbm_ActGearOdd'] != 'gN') & (Raw_Data['iom_VSP16'] > 5)]
    Max_Odd_Data = Odd_Data['dmm_GRincorrDiff1'].groupby(Raw_Data['gbm_ActGearOdd']).max()
    Min_Odd_Data = Odd_Data['dmm_GRincorrDiff1'].groupby(Raw_Data['gbm_ActGearOdd']).min()
    Even_Data = Raw_Data[(Raw_Data['rbm_TTCur'] == 2) & (Raw_Data['gbm_ActGearEven'] != 'gN') & (Raw_Data['iom_VSP16'] > 5)]
    Max_Even_Data = Even_Data['dmm_GRincorrDiff2'].groupby(Raw_Data['gbm_ActGearEven']).max()
    Min_Even_Data = Even_Data['dmm_GRincorrDiff2'].groupby(Raw_Data['gbm_ActGearEven']).min()
    All_Max_Data = pd.concat([Max_Odd_Data, Max_Even_Data], axis=0).sort_index(axis=0)
    All_Min_Data = pd.concat([Min_Odd_Data, Min_Even_Data], axis=0).sort_index(axis=0)
    Final_Data = pd.DataFrame({'Max': All_Max_Data.round(1), 'Min' : All_Min_Data}) #소숫점 첫번째 자리 반올림
    # Final_Data.index = pd.Index(Final_Data.index,name='Gear')
    print(Final_Data.columns)
    Final_Data.columns = pd.MultiIndex.from_product([['Error(Input Speed-Sychron Speed)[rpm]'], Final_Data.columns],
                                                    names=["", "Gear"])

    print(Raw_Data)
    print(type(Max_Odd_Data))
    print(Max_Odd_Data)
    print(type(Odd_Data['dmm_GRincorrDiff1']))
    print(Odd_Data['dmm_GRincorrDiff1'].count())

    # factor1 = pd.cut(Odd_Data['dmm_GRincorrDiff1'],3)
    factor1 = pd.cut(Odd_Data['dmm_GRincorrDiff1'], [-300,-100,0,100,300],include_lowest=True)
    print(factor1)
    print(type(factor1))
    # grouped_Odd_Data = Odd_Data['dmm_GRincorrDiff1'].groupby(factor1)
    grouped_Odd_Data= Odd_Data[['dmm_GRincorrDiff1','gbm_ActGearOdd']].groupby([factor1,'gbm_ActGearOdd'])
    print('grouped Data :',grouped_Odd_Data)
    print(grouped_Odd_Data.agg(['max','min']))
    print(grouped_Odd_Data.agg(['max', 'min']).T)
    print('==============================')
    print(grouped_Odd_Data.count()*0.01)
    print(grouped_Odd_Data.count().T * 0.01)
    grouped_Odd_Data_D = grouped_Odd_Data.count()
    grouped_Odd_Data_D_unstack= grouped_Odd_Data_D.unstack(0)
    print(grouped_Odd_Data_D_unstack)
    print(type(grouped_Odd_Data.count()))
    print(grouped_Odd_Data.count().index)
    # Final_Data.style.format(precision=0)

    ''' set.table_Styles
        - CSS Selector는 HTML element Style 주는 역할 전체 Table(행,열)을 정렬함
        - * : table 모든 요소
        - th : table head 약자(표의 제목 사용) / 기본 값 : 굵은 글씨체, 중앙정렬 
        - tr : table row 약자(가로줄) / 기본 값 : 보통 글씨체, 왼쪽정렬 
        - td : table data 약자(셀) / 기본 값 : 보통 글씨체, 왼쪽정렬'''

    all_props = [
        ('line-height', '1.5'),
        ('border', '2px solid #ccc'),
        ('boder-bottom','5px dash'),
        ('margin', '20px'),
    ]

    th_props = [
        ('box-sizing', 'content-box'),
        # ('padding', '20px'),
        ('width', '200px'),
        ('font-size','15px'),
        ('text-align', 'center'),
        ('font-weight', 'bold'),
        ('color', '#6d6d6d'),
        ('background-color','#e7708d'),
        # ('margin','20px'),
        # ('line-height', '1.0'),
        ('border', '2px solid #ccc'),
        ]

    thead_th = [

    ]

    tbody_th =[

    ]

    td_props = [
        ('font-size', '13px'),
        ('line-height', '1.2'),
        ('text-align', 'center'),
        ('border', '2px solid #ccc'),
        ]

    udf_highmax_props = [
        ('color', 'white'),
        ('background-color', 'lightcoral'),
    ]

    print("------------------------------------------")
    print(Final_Data.columns.get_loc(('Error(Input Speed-Sychron Speed)[rpm]', 'Max')))
    print(Final_Data.columns.get_loc(('Error(Input Speed-Sychron Speed)[rpm]', 'Min')))
    print(Final_Data.columns.get_loc('Error(Input Speed-Sychron Speed)[rpm]'))

    print(Final_Data)
    print(type(Final_Data[('Error(Input Speed-Sychron Speed)[rpm]', 'Max')]))

    def highlight_max(x, props=''):
        return np.where(x == np.nanmax(x.to_numpy()), props, '') # np.where (조건 문, 참일 때 값, 거짓 일 때 값)으로 반환
    def highlight_min(x, props=''):
        return np.where(x == np.nanmin(x.to_numpy()), props, '')

    print(Final_Data.to_numpy())
    print(Final_Data.iloc[:,[0,1]]) # [0,1]에서 [] (멀티인덱스라면) 가장 하위 레벨의 열을 선택 함. (활용도) 멀티인덱스 시, 특정열 선택 / 연속하지 않은 특정열 선택
    print(Final_Data.iloc[:, [0]])
    print(Final_Data.iloc[:,:])
    print(Final_Data.iloc[:, ])
    print(Final_Data.iloc[:-1, ])
    print(Final_Data[('Error(Input Speed-Sychron Speed)[rpm]', 'Max')])


    build = lambda x : pd.DataFrame(x, index = Final_Data.index, columns= Final_Data.columns)
    # udf_highmax_cls = build(Final_Data.iloc[:,[0]].apply(highlight_max, props ='udf_highmax_cls'))
    udf_highmax_cls = build(Final_Data.iloc[:,[0]].apply(highlight_max, props='udf_highmax_cls '))
    styles = [
        # dict(selector = "('Error(Input Speed-Sychron Speed)[rpm]', 'Max')")
        # dict(selector = "*", props = all_props),
        # dict(selector = "th:not(.index_name)", props = th_props),
        # dict(selector = "th.col_heading.level1", props = [('font-size','1.5em')]),
        # dict(selector=".index_name", props=th_props),
        dict(selector = "th.index_name.level1", props=th_props), # Level O이 가장 상위의 Index
        dict(selector = "th.col_heading.level1", props=th_props),
        dict(selector = "th.row_heading", props=th_props),
        dict(selector = "th.col_heading.level1.col1", props = [('background-color','#67c5a4')]),
        dict(selector = "th.row_heading.level0.row3", props=[('background-color', '#67c5a4')]),
        dict(selector = "td", props = td_props),
        dict(selector = "caption", props = [('caption-side','bottom'),('font-size','1.25em')]),
        dict(selector=".udf_highmax_cls", props=udf_highmax_props),
        # lux5 = dict(A=[dict(selector='', props=[('color', 'red')])])
        # {('Error(Input Speed-Sychron Speed)[rpm]', 'Max'):[{'selector': 'td', 'props': [('color', 'red')]}]}
        # dict(selector = "")
    ]

    styles_Max = [
        dict(selector=".udf_highmax_cls", props=udf_highmax_props),
    ]

    print(Final_Data.columns)

    Final_Data.loc[:'g3'].style.format(precision=1)
    Final_Data = Final_Data.style\
        .set_properties(**{'text-align': 'left'})\
        .format(precision=2) \
        .set_caption("TEST") \
        .set_td_classes(udf_highmax_cls) \
        .set_table_styles(styles,overwrite=False) \
        .set_table_styles({('Error(Input Speed-Sychron Speed)[rpm]', 'Max'): styles_Max}, overwrite=False)  # 특정열에 Style 적용을 위해선 {} , Documantation 참조할 것
        # .set_table_styles({('Error(Input Speed-Sychron Speed)[rpm]'): styles_Max}, overwrite=False) \

    ''' 셀 배경색 변경 '''
    # def draw_color_cell(x,color) :
    #     color = f'background-color : {color} '
    #     return color
    # .apply(draw_color_cell, color='#ff9090', subset=pd.IndexSlice['g1'])

    ''' Multi Inex 사용 시 예, {:.1f}의 경우, 모든 열에 해당 함.'''
    #.format('{:.1f}',subset=[('Error(Input Speed-Sychron Speed)[rpm]', 'Max'),
    #                          ('Error(Input Speed-Sychron Speed)[rpm]', 'Min')]) \
    ''' '''
    #  .set_table_styles([ dict(selector='th',
    #                      props=[('text-align', 'center'), ('font-size','18px'), ('margin','10px')])])
    # props=[('text-align', 'center'), ('font-size','18px'), ('margin','10px')])])
    # print(Final_Data)
    dfi.export(Final_Data, '새로운 표1.jpg')

    # time.sleep(5)

    '''Picture Remove'''
    # os.remove('새로운 표1.png')

    '''DataFrame Index / Columns 확인'''
    # print(Final_Data.index, Final_Data.columns)

    '''DataFrame 내 특정(열) / 특정(데이터) 선택'''
    # Test_Data = Raw_Data[Raw_Data['gbm_ActGearOdd'] != 'gN']
    # Test_Data1 = Raw_Data[Raw_Data['gbm_ActGearOdd'].isin(['g1','g3'])]
    ''' '''

    '''Series 데이터 선택'''
    # print(Max_Data,type(Max_Data))
    # print(Max_Data[0:3])
    ''' '''



    All_Max_Data.to_csv('Data Visual_T.csv',index=True)
    # Test_Data1.to_csv('Data Visu.csv', index=False)
    # MyDataFrame.to_csv('Data Visual.csv',index=False)