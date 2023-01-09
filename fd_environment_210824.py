import numpy as np
import pandas as pd
import dataframe_image as dfi
import ansiglist
import collections, numpy

'''
1. Shift Gear 체결빈도
2. Select Direction 체결빈도
   - Odd H/L
   - Even H/L
3. MCU Temp 그래프 / Max 온도 / 평균 온도 :  iom_Mcu_MotTemp_C
4. Slope 그래프 : Slope
/5. CPU Load 분포 / Max CPU Load : Os_GusCPULoad_[0]/[1]/[2]
6. Brake On/Off 비율 : BrakeSwitchLocal
7. 전체 주행 시간
8. 전체 주행 거리(odometer) : iom_Clu_Odometer
9. Clutch Drive Gear Shift 횟수 및 Control Time 비율 : csm_DrivingGear
10. Clutch Shift 횟수 (삭제) Clutch Motor Turn On Count Count
/11. Clutch Motor Turn On Contol Time
12. 고도(height) Min / Max / Mean : ALTITUDE
13. 외기온 평균 값 : CR_Fatc_OutTemp
14. APS 비율 : APS
15. 차속 비율 : iom_VSP16
'''

def run(AnalySig):
    ''' 15. 차속비율 '''
    vehicle_speed_interval = pd.cut(AnalySig['iom_VSP16'],[0,30,50,70,90,120,180], right=False, include_lowest=True,precision=2) # 1번인자 : 배열 / 2번인자 : 구간 / right : < A << / inclue_lowest = True 최소 값 포함 여부
    Analy_15 = AnalySig['iom_VSP16'].groupby([vehicle_speed_interval]).count()*0.01
    Analy_15['Driving Total Time'] = AnalySig['iom_VSP16'].count()*0.01
    print(Analy_15)

    ''' 14. APS 비율 (0을 제외)'''
    APS_interval = pd.cut(AnalySig['APS'],[0,10,20,30,40,50,70,100], right=True, include_lowest=False,precision=2) # 1번인자 : 배열 / 2번인자 : 구간 / right : < A << / inclue_lowest = True 최소 값 포함 여부
    Analy_14 = AnalySig['APS'].groupby([APS_interval]).count()*0.01
    print(Analy_14)

    ''' 13. 외기온 평균 '''
    Analy_13 = AnalySig['CR_Fatc_OutTemp'].mean()
    Analy_13 = pd.DataFrame([Analy_13],index=['outside air temp.'])
    print(Analy_13)

    ''' 12. 고도(height) Min / Max / Mean : ALTITUDE '''
    height_min = AnalySig['ALTITUDE'].min()
    height_max = AnalySig['ALTITUDE'].max()
    height_mean = AnalySig['ALTITUDE'].mean()
    Analy_12 = pd.Series([height_min,height_max,height_mean],index=['height_min','height_max','height_mean'])
    print(Analy_12)

    ''' 10. Clutch Shift 횟수 : csm_DrivingGear '''
    clutch_Shift_gear_change = []
    i=0
    while i < len(AnalySig['csm_DrivingGear'])-1:
        if i==0:
            clutch_Shift_gear_change.append(AnalySig['csm_DrivingGear'][i])
        if AnalySig['csm_DrivingGear'][i+1] != AnalySig['csm_DrivingGear'][i]:
            if AnalySig['csm_DrivingGear'][i] == 'g1'or AnalySig['csm_DrivingGear'][i] == 'g3'or AnalySig['csm_DrivingGear'][i] =='g5':
                if AnalySig['csm_DrivingGear'][i+1] == 'g2'or AnalySig['csm_DrivingGear'][i+1] == 'g4'or AnalySig['csm_DrivingGear'][i+1] =='g6':
                    clutch_Shift_gear_change.append(AnalySig['csm_DrivingGear'][i+1])
            if AnalySig['csm_DrivingGear'][i] == 'g2'or AnalySig['csm_DrivingGear'][i] == 'g4'or AnalySig['csm_DrivingGear'][i] =='g6':
                if AnalySig['csm_DrivingGear'][i+1] == 'g1'or AnalySig['csm_DrivingGear'][i+1] == 'g3'or AnalySig['csm_DrivingGear'][i+1] =='g5':
                    clutch_Shift_gear_change.append(AnalySig['csm_DrivingGear'][i+1])
        i+=1

    clutch_Shift_gear_change = pd.DataFrame(clutch_Shift_gear_change,columns=['clutch_Shift_gear_change'])
    odd_clutch_Shift_count = clutch_Shift_gear_change[(clutch_Shift_gear_change['clutch_Shift_gear_change']=='g1')|
                                                      (clutch_Shift_gear_change['clutch_Shift_gear_change']=='g3')|
                                                      (clutch_Shift_gear_change['clutch_Shift_gear_change']=='g5')].count()

    even_clutch_Shift_count = clutch_Shift_gear_change[(clutch_Shift_gear_change['clutch_Shift_gear_change']=='g2')|
                                                      (clutch_Shift_gear_change['clutch_Shift_gear_change']=='g4')|
                                                      (clutch_Shift_gear_change['clutch_Shift_gear_change']=='g6')].count()

    Analy_10 = pd.Series([odd_clutch_Shift_count['clutch_Shift_gear_change'],even_clutch_Shift_count['clutch_Shift_gear_change']],index=['odd_clutch_Shift_count','even_clutch_Shift_count'])
    Analy_10['clutch_shift_count'] = len(clutch_Shift_gear_change)
    print(Analy_10)

    ''' 9. Clutch Drive Gear Shift 횟수 및 Control Time 비율 : csm_DrivingGear '''
    ''''9-1 Clutch Drive gear별 Shift 횟수 '''
    clutch_Shift_gear_change = []
    i=0
    while i < len(AnalySig['csm_DrivingGear'])-1:
        if i==0:
            clutch_Shift_gear_change.append(AnalySig['csm_DrivingGear'][i])
        if AnalySig['csm_DrivingGear'][i+1] != AnalySig['csm_DrivingGear'][i]:
            clutch_Shift_gear_change.append(AnalySig['csm_DrivingGear'][i+1])
        i+=1

    clutch_each_gear_count = collections.Counter(clutch_Shift_gear_change)
    clutch_each_gear_count = pd.DataFrame.from_dict([clutch_each_gear_count]).T
    clutch_each_gear_count.sort_index(inplace=True)
    clutch_each_gear_count.columns=['clutch_each_gear_count']

    ''' 9-2 Clutch Control Time 비율 '''
    clutch_each_gear_ContTime = collections.Counter(AnalySig['csm_DrivingGear'])
    clutch_each_gear_ContTime = pd.DataFrame.from_dict([clutch_each_gear_ContTime]).T
    clutch_each_gear_ContTime.sort_index(inplace=True)
    clutch_each_gear_ContTime=clutch_each_gear_ContTime*0.01
    clutch_each_gear_ContTime.columns=['clutch_each_gear_ContTime']

    print(clutch_each_gear_count)
    print(clutch_each_gear_ContTime)

    Analy_9 = pd.concat([clutch_each_gear_count,clutch_each_gear_ContTime],axis=1) #axis=1 열방향으로 합치기
    print(Analy_9)

    ''' 8. 전체주행 거리 '''
    Analy_8= AnalySig['iom_Clu_Odometer'][len(AnalySig['iom_Clu_Odometer'])-1] - AnalySig['iom_Clu_Odometer'][0]
    Analy_8 = pd.DataFrame([Analy_8],index=['vehicle mileage'])
    print(Analy_8)


    ''' 7. 전체주행 시간 '''
    Analy_7 = AnalySig['time'][len(AnalySig['time'])-1]
    Analy_7 = pd.DataFrame([Analy_7], index=['vehicle drving time'])
    print(Analy_7)

    ''' 6. Brake On/Off 비율 '''
    brake_on = AnalySig[AnalySig['BrakeSwitchLocal']=="BS_BrakeON"]['BrakeSwitchLocal'].count()*0.01
    brake_off = AnalySig[AnalySig['BrakeSwitchLocal']=="BS_BrakeOFF"]['BrakeSwitchLocal'].count()*0.01
    Analy_6 = pd.Series([brake_on,brake_off],index=['brake on','brake off'])
    print(Analy_6)

    ''' 4. Slope 구간별 비율 : Slope '''
    Slope_interval = pd.cut(AnalySig['Slope'],[-20,-10,-5,-3,0,3,5,10,20], right=True, include_lowest=False,precision=2) # 1번인자 : 배열 / 2번인자 : 구간 / right : < A << / inclue_lowest = True 최소 값 포함 여부
    Analy_4 = AnalySig['Slope'].groupby([Slope_interval]).count()*0.01
    print(Analy_4)

    ''' 3. MCU Temp 그래프 / Max 온도 / 평균 온도 :  iom_Mcu_MotTemp_C '''
    mcu_temp_max = AnalySig['iom_Mcu_MotTemp_C'].max()
    mcu_temp_mean = AnalySig['iom_Mcu_MotTemp_C'].mean()
    Analy_3 = pd.DataFrame([mcu_temp_mean,mcu_temp_max],index=['mcu_temp_mean','mcu_temp_max'])
    print(Analy_3)

    ''' 2. Select Direction 체결빈도(Odd H/L, Even H/L) '''
    odd_H_sel_count = []
    odd_L_sel_count = []
    even_H_sel_count = []
    even_L_sel_count = []
    i=0
    while i < len(AnalySig['gam_SelActPos1']):
        if AnalySig['gam_SelActPos1'][i] == 0:
            while True:
                i+=1
                if AnalySig['gam_SelActPos1'][i] == 7:
                    odd_H_sel_count.append(1)
                    break
                if i == len(AnalySig['gam_SelActPos1'])-1:
                    break
        if AnalySig['gam_SelActPos1'][i] == 7:
            while True:
                i+=1
                if AnalySig['gam_SelActPos1'][i] == 0:
                    odd_L_sel_count.append(1)
                    break
                if i == len(AnalySig['gam_SelActPos1'])-1:
                    break
        i+=1

    i=0
    while i < len(AnalySig['gam_SelActPos2']):
        if AnalySig['gam_SelActPos2'][i] == 0:
            while True:
                i+=1
                if AnalySig['gam_SelActPos2'][i] == 7:
                    even_H_sel_count.append(1)
                    break
                if i == len(AnalySig['gam_SelActPos2'])-1:
                    break
        if AnalySig['gam_SelActPos2'][i] == 7:
            while True:
                i+=1
                if AnalySig['gam_SelActPos2'][i] == 0:
                    even_L_sel_count.append(1)
                    break
                if i == len(AnalySig['gam_SelActPos2'])-1:
                    break
        i+=1

    Analy_2 = pd.DataFrame([len(odd_L_sel_count),len(odd_H_sel_count),len(even_L_sel_count),len(even_H_sel_count)],
                           index=['odd_L_sel_count', 'odd_H_sel_count', 'even_L_sel_count', 'even_H_sel_count'])
    print(Analy_2)

    ''' 1. Shift Gear 체결빈도 
         [Search 방법]
          : gN이 아닐 영역을 sorting하고 첫번째 값은 저장하고 이후, index 값이 연속적이지 않을 경우의 i+1 값을 저장함. 
    '''

    sfcon_odd = AnalySig[(AnalySig['rbm_TTCur']==2) & (AnalySig['gbm_ActGearOdd']!='gN')]
    sfcon_even = AnalySig[(AnalySig['rbm_TTCur']==2) & (AnalySig['gbm_ActGearEven']!='gN')]
    odd_shift_change_gear = []
    even_shift_change_gear = []
    i=0
    while i < len(sfcon_odd['gbm_ActGearOdd'])-1:
        if i==0:
            odd_shift_change_gear.append(sfcon_odd['gbm_ActGearOdd'].iloc[i])
        if sfcon_odd.index[i+1] !=sfcon_odd.index[i]+1:
            odd_shift_change_gear.append(sfcon_odd['gbm_ActGearOdd'].iloc[i+1])
        i+=1

    i=0
    while i < len(sfcon_even['gbm_ActGearEven'])-1:
        if i==0:
            even_shift_change_gear.append(sfcon_even['gbm_ActGearEven'].iloc[i])
        if sfcon_even.index[i+1] !=sfcon_even.index[i]+1:
            even_shift_change_gear.append(sfcon_even['gbm_ActGearEven'].iloc[i+1])
        i+=1

    odd_shift_change_gear_collection = collections.Counter(odd_shift_change_gear)
    odd_shift_change_gear_collection = pd.DataFrame.from_dict([odd_shift_change_gear_collection]).T

    even_shift_change_gear_collection = collections.Counter(even_shift_change_gear)
    even_shift_change_gear_collection = pd.DataFrame.from_dict([even_shift_change_gear_collection]).T

    all_shift_change_gear_collection = pd.concat([odd_shift_change_gear_collection,even_shift_change_gear_collection],axis=0).sort_index(axis=0)
    all_shift_change_gear_collection.columns=['Shift Gear Chanage Count']
    Analy_1 = all_shift_change_gear_collection
    print(Analy_1)


    print(Analy_1.shape[0], type(Analy_1.shape[0]))
    print(Analy_1.shape[1], type(Analy_1.shape[1]))


    Analy = [Analy_1,Analy_2,Analy_3,Analy_4,Analy_6,Analy_7,Analy_8,Analy_9,Analy_10,Analy_12,Analy_13,Analy_14,Analy_15]

    ''' export excel '''
    fd_environment_Analy = Analy

    return (fd_environment_Analy)