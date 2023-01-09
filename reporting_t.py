import os
import numpy as np
import pandas as pd
import win32com.client, sys
from win32com.client import Dispatch


def run(report_info):
    ''' PPT 기본 설정'''
    PowerPoint = win32com.client.Dispatch("PowerPoint.Application")
    PowerPoint.Visible = True # Background process
    PowerPoint.DisplayAlerts = 0  # No display, no warning
        # PPT File Open을 통한 보고서 작성 시 사용
        # prs = PowerPoint.Presentations.Open(pptx_fpath, ReadOnly= False, WithWindow=False)

    # PPT 신규 파일 생성 / Slide 사이즈 / 사용자 테마 적용
    Presentation = PowerPoint.Presentations.Add() # 최종 presentation (obj) Return
    Presentation.PageSetup.SlideSize = 0x03 # A4 size로 변경
    Presentation.ApplyTheme("C:\\Users\\Administrator\\AppData\\Roaming\\Microsoft\\Templates\\Document Themes\\보고서 자동화_TEST.thmx")

    # 사용자 Layout 속성 지정
    title_layout = Presentation.SlideMaster.CustomLayouts(1) #custom layout for a slide 반환
    ct1_layout = Presentation.SlideMaster.CustomLayouts(2) # 좌/우 그림 추가 포맷
    ct2_layout = Presentation.SlideMaster.CustomLayouts(3) # 상/하 그림 추가 포맷

    # 레포트 표지 정보 입력
    Presentation.Slides.AddSlide(1,title_layout) #AddSlide의 첫번째 인자 (Slide Index), 두번째 인자는 custom Layout만 들어가야 함.
    i = 0
    while i < len(report_info)-1:
        Presentation.Slides(1).Shapes(i+1).TextFrame.TextRange.Text = report_info[i]
        i +=1
    ''' '''


    Presentation.Slides.AddSlide(Presentation.Slides.Count+1,ct2_layout)
    Presentation.Slides.AddSlide(Presentation.Slides.Count+1,ct2_layout)


    # shape_index ={}
    # for i, shape in enumerate(Presentation.Slides(1).Shapes): #enumerate : 리스트의 순서(i)와 리스트 값(shape)을 전달
    #     shape_index[ shape.name ] = i
    # print(pd.Series(shape_index))

    current_path = os.getcwd().replace('/','\\') + '\\'
    add_image_1 = 'fd_gri1.png'
    add_image_2 = 'fd_gri2.png'
    add_image_3 = 'fd_sge1.png'
    add_image_4 = 'fd_sge2.png'

    print(current_path+add_image_1)
    Presentation.Slides(2).Shapes(1).TextFrame.TextRange.Text = 'TEST 중, Gear Ratio Incorrection'
    Presentation.Slides(2).Shapes.AddPicture(current_path + add_image_1, False, True, 0, 0)
    Presentation.Slides(2).Shapes.AddPicture(current_path + add_image_2, False, True, 0, 0)


    Presentation.Slides(3).Shapes(1).TextFrame.TextRange.Text = 'TEST 중, Shift Gear Engage Stuck'
    Presentation.Slides(3).Shapes.AddPicture(current_path + add_image_3, False, True, 0, 0)
    Presentation.Slides(3).Shapes.AddPicture(current_path + add_image_4, False, True, 0, 0)
    os.remove(add_image_1)
    # os.remove(add_image_2)

    # Slides Shape name 확인을 위한 코드-------------------------
    shape_index = {}
    for i, shape in enumerate(Presentation.Slides(2).Shapes):  # enumerate : 리스트의 순서(i)와 리스트 값(shape)을 전달
        shape_index[shape.name] = i
    print(pd.Series(shape_index))
    #-----------------------------------------------------------

    Presentation.SaveAs(current_path + report_info[4])
    Presentation.Close()
    PowerPoint.Quit()
    return()