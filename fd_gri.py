import numpy as np
import pandas as pd
import  dataframe_image as dfi

'''
[Gear Ratio Incorrection 진단]
    <조건> : 시동상태 & 차속 > 5KPH
    1. 각 기어단별 Max/Min Synchron Speed 확인 
        : 전체 기어단에서 Max/Min Sychron Speed 표시
    2. 기어단별 Error Speed 구간별 측정 시간 확인
       [참고] sychron Error
       g1 : 500 / g2 : 400 / g3 : 200 / g4 : 200 / g5 : 200 / g6 : 200
'''
def run(AnalySig) :
    ''' 기어단별 Error(Input Speed - Synchron Speed) [rpm] 최대/최소 값 확인 '''
    sfcon_odd = AnalySig[(AnalySig['rbm_TTCur'] == 2) & (AnalySig['gbm_ActGearOdd'] != 'gN') & (AnalySig['iom_VSP16'] > 5)]
    sfcon_even = AnalySig[(AnalySig['rbm_TTCur'] == 2) & (AnalySig['gbm_ActGearEven'] != 'gN') & (AnalySig['iom_VSP16'] > 5)]
    max_odd_synchron = sfcon_odd['dmm_GRincorrDiff1_rpm'].groupby(sfcon_odd['gbm_ActGearOdd']).max()
    max_even_synchron = sfcon_even['dmm_GRincorrDiff2_rpm'].groupby(sfcon_even['gbm_ActGearEven']).max()
    min_odd_synchron = sfcon_odd['dmm_GRincorrDiff1_rpm'].groupby(sfcon_odd['gbm_ActGearOdd']).min()
    min_even_synchron = sfcon_even['dmm_GRincorrDiff2_rpm'].groupby(sfcon_even['gbm_ActGearEven']).min()
    max_all_gear_synchron = pd.concat([max_odd_synchron, max_even_synchron], axis=0).sort_index(axis=0) # 홀수/짝수 Max Synchron Speed를 (행방향)으로 붙이고 (행방향) 정렬
    min_all_gear_synchron = pd.concat([min_odd_synchron, min_even_synchron], axis=0).sort_index(axis=0)

    Analy_table_1 = pd.DataFrame({'Max': max_all_gear_synchron, 'Min': min_all_gear_synchron})
    Analy_table_1.columns = pd.Index(Analy_table_1.columns, name='Gear') #Index name 설정(Index Label이 아님) / Multi Index 시 유용할 듯

    #[중요]
    # add_data= pd.DataFrame([['추가 데이터', '추가 데이터']], columns=Analy_table_1.columns, index=['추가'])
    # Analy_table_1 = Analy_table_1.append(add_data)

    ''' 기어단별 Error 구간별 측정 시간 확인 '''
    odd_spd_err_time_interval = pd.cut(sfcon_odd['dmm_GRincorrDiff1_rpm'],[-500,-300,-200,-100,0,100,200,300,500], right=False, include_lowest=True,precision=2) # 1번인자 : 배열 / 2번인자 : 구간 / right : < A << / inclue_lowest = True 최소 값 포함 여부
    odd_interval_spd_err_totaltime = sfcon_odd[['dmm_GRincorrDiff1_rpm','gbm_ActGearOdd']].groupby([odd_spd_err_time_interval,'gbm_ActGearOdd']).count()*0.01
    odd_interval_spd_err_totaltime = odd_interval_spd_err_totaltime.unstack(0) # 행인덱스의 0(최상위 인덱스)를 열인덱스로 바꿈
    odd_interval_spd_err_totaltime = odd_interval_spd_err_totaltime.rename(columns={'dmm_GRincorrDiff1_rpm':'Error_Speed'}) # columns label 이름 변경 / 아래와 같이 사용해도 무방(같은 이름을 level0, level1 이 동시에 사용 시에 아래 사용이 나을 듯함)
    # odd_interval_spd_err_totaltime.columns.set_levels(['error_speed'], level=0, inplace= True)
    even_spd_err_time_interval = pd.cut(sfcon_even['dmm_GRincorrDiff2_rpm'],[-500, -300, -200, -100, 0, 100, 200, 300, 500], right=False, include_lowest=True,precision=2)  # 1번인자 : 배열 / 2번인자 : 구간 / right : < A << / inclue_lowest = True 최소 값 포함 여부
    even_interval_spd_err_totaltime = sfcon_even[['dmm_GRincorrDiff2_rpm', 'gbm_ActGearEven']].groupby([even_spd_err_time_interval, 'gbm_ActGearEven']).count()*0.01
    even_interval_spd_err_totaltime = even_interval_spd_err_totaltime.unstack(0)  # 행인덱스의 0(최상위 인덱스)를 열인덱스로 바꿈
    even_interval_spd_err_totaltime = even_interval_spd_err_totaltime.rename(columns={'dmm_GRincorrDiff2_rpm': 'Error_Speed'})
    all_gear_interval_spd_error_totaltime = pd.concat([odd_interval_spd_err_totaltime, even_interval_spd_err_totaltime], axis=0).sort_index(axis=0)  # 홀수/짝수 Max Synchron Speed를 (행방향)으로 붙이고 (행방향) 정렬
    all_gear_interval_spd_error_totaltime = all_gear_interval_spd_error_totaltime['Error_Speed'] #[중요] 최상위 Level의 열을 삭제하기 위해서, 원래 용도는 MultiIndex의 특정 열을 선택하는 목적
    all_gear_interval_spd_error_totaltime.columns = ['[∞,-300]rpm','[-300,-200]rpm', '[-200,-100]rpm', '[-100,0]rpm','[0,100]rpm','[100,200]rpm','[200,300]rpm','[300,∞]rpm'] # 특정 열의 라벨 이름을 변경하기보다 전체적으로 바꾸고자 할 때 사용
    all_gear_interval_spd_error_totaltime.columns.name='Gear'
    # all_gear_interval_spd_error_totaltime.index.name = 'A' : index 이름 지정

    i=0
    add_data_1 = pd.Series([])
    while i < len(all_gear_interval_spd_error_totaltime.columns):
        add_data_1 = add_data_1.append(all_gear_interval_spd_error_totaltime.iloc[:,[i]].sum())
        i += 1
    add_data_1 = pd.DataFrame([add_data_1], columns=all_gear_interval_spd_error_totaltime.columns, index=['Sub Total Time'])
    add_data_2 = pd.DataFrame([[add_data_1.T.sum()[0],'','','','','','','']],columns=all_gear_interval_spd_error_totaltime.columns,index=['Total Time'])
     # [중요] 데이터프레임의 경우, sum()함수는 열기준으로 합산된다.
     # 여기서 반환하는 값은 Series 또는 DataFrame이 아니기에 sum()[0]으로 데이터를 반환해야 함. sum()만 반환할 경우, Series 전체 값이 반환됨.
     # 따라서 행의 합을 구하려면 상기와 같이 T를 사용하던 groupby를 이용해 구하고자하는 행을 열로 바꾼뒤에 합산을 구하면 된다.

    # print(add_data_1[0])
    print(add_data_2)
    Analy_table_2 = all_gear_interval_spd_error_totaltime.append(add_data_1)
    Analy_table_2 = Analy_table_2.append(add_data_2)
    print(Analy_table_2)


    ''' [참고] DataFrame 데이터 반올림 함수 : round '''
        # 파이썬에서는 ROUND_HALF_EVEN 방식을 사용하기 때문에 짝수에 가까운쪽으로 반올림을 함. 즉, 0,5 > 0 / 1.5 > 2
        # 따라서 DataFrame을 이미지로 추출하고자 할 때는 원본 데이터(DataFrame)를 수정하는 것보다
        # 추출할 이미지(DataFrame.Style)에서 변경하는 쪽이 낫다.
        # <round함수 사용 예>
        # pd.DataFrame({'Max': max_all_gear_synchron.round(1), 'Min': min_all_gear_synchron.round(2)})

    '''[참고] 분석한 DataFrame에 추가적인 분석 데이터나 코멘트를 DataFrame의 행에 추가하고 싶을 경우 '''
        # <상기 데이터를 통한 예시 : 마지막 행에 1개 추가>
        # add_data= pd.DataFrame([['추가 데이터', '추가 데이터']], columns=final_table.columns, index=['추가'])
        # final_table = final_table.append(add_data)


    '''최종 분석 Table(DataFrame)을 [이미지화 할 때] 특정 조건을 부여하기 위한 Fuction 모음'''
        #[주의사항 **]
        #최종 DataFrame에 추가 행을 통해 코멘트나 다른 분석 형태가 들어갈 경우에 분석을 구분 지어여 함. (중요)
    def highlight_max(x, props=''):
        return np.where(x == np.nanmax(x.to_numpy()), props, '') # np.where (조건 문, 참일 때 값, 거짓 일 때 값)으로 반환
    def highlight_min(x, props=''):
        return np.where(x == np.nanmin(x.to_numpy()), props, '')
    build = lambda x: pd.DataFrame(x, index=x.index, columns=x.columns)
        # return (build)

    # udf_highmax_cls = build(Analy_table_1.iloc[:-1 , [0]].apply(highlight_max, props='udf_highmax_cls')) # 주의사항 ** / iloc[  [0]] : 여기서 [0]은 특정 열을 선택함.
    udf_highmax_cls = build(Analy_table_1.iloc[:, [0]].apply(highlight_max, props='udf_highmax_cls'))
    udf_highmin_cls = build(Analy_table_1.iloc[:, [1]].apply(highlight_min, props='udf_highmin_cls'))

    ''' '''

    ''' 추출할 이미지 스타일 설정 '''
        # selector
        #   - CSS Selector를 참조 :  HTML element Style 주는 역할로 Table 내 세부 영역을 구분함.
        #   - Slector 기본 종류
        #       * : table 모든 요소
        #       th : table head 약자(표의 제목 사용) / 기본 값 : 굵은 글씨체, 중앙정렬
        #       tr : table row 약자(가로줄) / 기본 값 : 보통 글씨체, 왼쪽정렬
        #       td : table data 약자(셀) / 기본 값 : 보통 글씨체, 왼쪽정렬

    ''' [참고] CSS Style '''
    # ('line-height', '1.5'),
    # ('border', '2px solid #ccc'), : 테두리 설정하는 속성으로 속성을 한꺼번에 사용 가능(width-style-color 순으로 작성)
    # ('border-bottom', '5px dash' or 'dotted','royalblue'),
    # ('border-top', '5px dash'),
    # ('border-left', '5px dash'),
    # ('border-right', '5px dash'),
    # ('box-sizing', 'content-box'),
    # ('display', 'none'),
    # ('display.block', '300p'),
    # ('width', '200px'),
    # ('height', '200px'),
    # ('font-size', '15px'),
    # ('text-align', 'center'),
    # ('font-weight', 'bold'),
    # ('color', '#6d6d6d'), : 'salmon' / 'lightcoral' / 'silver' / 'white' / 'lightgreen' / 'royalblue'
    # ('background-color', '#e7708d'),
    # ('border', '2px solid #ccc'),
    # ('padding', '20px'), : 안쪽 여백
    # ('margin', '20px'), : 바깥쪽 여백

    caption_props = [
        ('caption-side','top'),
        ('font-size','15px'),
        ('font-weight','bold'),
        # ('color', 'darkblue'),
        ('width', '300px'),
        ('text-align', 'center'), #[중요] caption의 길이가 너무 길어 실제 분석 테이블의 행 인덱스와 열 인덱스, 데이터 영역이 길어지는 경우가 있음. 이 때는 caption 전체 길이에 행/열 인덱스에 설정된 비율로 정해짐.
        ('padding', '8px'),
    ]

    th_index_name_props = [
        ('text-align', 'center'),
        ('border', '1px solid black'),
        # ('color', ''),
        ('background-color', 'lightgoldenrodyellow'),
        ('font-size', '15px'),
    ]

    th_row_heading_props = [
        ('text-align', 'center'),
        ('border', '1px solid black'),
        ('font-size', '15px'),
        ('width', '60px'),
    ]

    th_col_heading_props = [
        ('text-align', 'center'),
        ('border', '1px solid black'),
        ('font-size', '15px'),
        ('background-color', 'lightgoldenrodyellow'),
        # ('width', '30px'),
    ]

    th_td_props = [
        ('text-align', 'center'),
        ('border', '1px solid black'),
        ('font-size', '15px'),
        ('width', '80px'),
    ]

    udf_highmax_cls_props = [
        ('background-color', 'lightcoral'),
        ('font-weight', 'bold'),
        ('color', 'white')
    ]

    udf_highmin_cls_props = [
        ('background-color', 'royalblue'),
        ('font-weight', 'bold'),
        ('color', 'white')
    ]
    styles_1 = [
        dict(selector='caption', props=caption_props),
        dict(selector='th.index_name', props=th_index_name_props),
        dict(selector='th.row_heading', props=th_row_heading_props),
        dict(selector='th.col_heading', props=th_col_heading_props),
        dict(selector='td', props=th_td_props),
        dict(selector='.udf_highmax_cls', props=udf_highmax_cls_props),
        dict(selector='.udf_highmin_cls', props=udf_highmin_cls_props),
        # dict(selector='*', props=),
        # dict(selector='th:not(.index_name)', props=), #th 중, index.name을 제외하고 모두
        # dict(selector='th.index_name.level1', props=),
        # dict(selector='th.row_heading.level0.col1', props=), #level0은 가장 상위의 Index, multiindex시 활용
        # dict(selector='th.col_heading.level0.row3', props=),
    ]

    styles_2 = [
        dict(selector='caption', props=caption_props),
        dict(selector='th.index_name', props=th_index_name_props),
        dict(selector='th.row_heading', props=th_row_heading_props),
        dict(selector='th.col_heading', props=th_col_heading_props),
        dict(selector='td', props=th_td_props),
        dict(selector='.udf_highmax_cls', props=udf_highmax_cls_props),
        dict(selector='.udf_highmin_cls', props=udf_highmin_cls_props),
        # dict(selector='*', props=),
        # dict(selector='th:not(.index_name)', props=), #th 중, index.name을 제외하고 모두
        # dict(selector='th.index_name.level1', props=),
        # dict(selector='th.row_heading.level0.col1', props=), #level0은 가장 상위의 Index, multiindex시 활용
        # dict(selector='th.col_heading.level0.row3', props=),
    ]


    Analy_table_image_1 = Analy_table_1.style\
        .format(precision=1)\
        .set_caption("Error(Input Speed-Synchron Speed) [rpm]")\
        .set_table_styles(styles_1) \
        .set_td_classes(udf_highmax_cls)\
        .set_td_classes(udf_highmin_cls)
        # .set_td_classes(udf_highmax_cls + udf_highmin_cls) \ # [중요] (동일한 데이터 영역)에 각각의 User Defined Class를 적용 시에만 +로 묶을 수 있다. 만약 각 Class의 분석하고자 하는 데이터 영역이 다르거나 분석하고자 하는 데이터 영역이 같고 분석 function도 동일 시에는 적용되지 않는다. 따라서 이 때는 분리해서 써줘야 함.

    Analy_table_image_2 = Analy_table_2.style \
        .format(precision=2) \
        .set_caption("Error(Input SPD - Sychron SPD) 구간별 측정 시간(sec)") \
        .set_table_styles(styles_2) \
        .set_td_classes(udf_highmax_cls) \
        .set_td_classes(udf_highmin_cls)
    # .set_td_classes(udf_highmax_cls + udf_highmin_cls) \ # [중요] (동일한 데이터 영역)에 각각의 User Defined Class를 적용 시에만 +로 묶을 수 있다. 만약 각 Class의 분석하고자 하는 데이터 영역이 다르거나 분석하고자 하는 데이터 영역이 같고 분석 function도 동일 시에는 적용되지 않는다. 따라서 이 때는 분리해서 써줘야 함.

    dfi.export(Analy_table_image_1, 'fd_gri1.png')
    dfi.export(Analy_table_image_2, 'fd_gri2.png')

    ''' export excel '''
    fd_gri_Analy = [Analy_table_1,Analy_table_2]

    return(fd_gri_Analy)