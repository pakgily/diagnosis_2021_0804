import os
import numpy as np
import pandas as pd
import win32com.client, sys
from win32com.client import Dispatch

pptx_fpath = 'D:/MyPythonProj/python_Data_analy/2021_0629_OBD/TEST_PPT_templete.pptx'
PowerPoint = win32com.client.Dispatch("PowerPoint.Application")
PowerPoint.Visible = True # Background process
# ppt.DisplayAlerts = 0  # No display, no warning
# prs = PowerPoint.Presentations.Open(pptx_fpath, ReadOnly= False, WithWindow=False)
PowerPoint.Presentations.Add.Slides.Add(1,)

prs = PowerPoint.Presentations.Open(pptx_fpath)
PowerPoint.ActivePresentation.ApplyTheme("C:\\Users\\Administrator\\AppData\\Roaming\\Microsoft\\Templates\\Document Themes\\Default Theme.thmx")










'''Picture Remove'''
# os.remove('새로운 표1.png')

All_Max_Data.to_csv('Data Visual_T.csv', index=False)


'''
Presentations.Open : option 중, WithWidows=Falase 일 경우, 
아래의 ActivePresenstation.ApplyTheme 적용 불가함.
'''



slide_num = 0
slide = prs.slides[slide_num] #[] 대괄호 대신 () 소괄호 사용 가능 이 때 첫번째 슬라이드는 1번부터 시작 함.
shapes_list = slide.shapes
shape_index = {} # 리스트 만들기
for i, shape in enumerate(shapes_list): #enumerate : 리스트의 순서(i)와 리스트 값(shape)을 전달
    shape_index[ shape.name ] = i
print(pd.Series(shape_index))

current_path = os.getcwd().replace('/','\\') + '\\'
add_image = '새로운 표1.png'
prs.Slides(2).Shapes.AddPicture(current_path+add_image,False,True,85,180) # 마지막 2개는 option으로 크기조정에 쓰임. 미기입 시, 원본 사이즈
prs.Slides(2).Shapes(1).TextFrame.TextRange.Text = 'Gear Ratio Incorrection 정합성 검증'

slide_layout2 = PowerPoint.ActivePresentation.Designs(1).SlideMaster.CustomLayouts(1)
placehold = slide_layout2.Shapes.Placeholders.Item(3)
print(slide_layout2.Shapes.Placeholders.Item(1).name)
oSlide1= PowerPoint.ActivePresentation.Slides.AddSlide(1,slide_layout2)
oShape1 = oSlide1.Shapes.Placeholders.Item(1)
print(oShape1.name)
print(oShape1.Left)

'''
슬라이드 마스터에 (내용 개체 틀) 삽입 시에 하기 AddPicture 위치 자표 입력 시에도 소용 없음. 자동 입력 됨.
'''
prs.Slides(1).Shapes.AddPicture(current_path+add_image,0,-1,100,13)
# prs.Slides(1).Shapes.AddPicture(current_path+add_image,0,-1,100,13)
# prs.Slides(1).Shapes.AddPicture(current_path+add_image,0,-1,100,13)
# prs.Slides(1).Shapes.AddPicture(current_path+add_image,0,-1,100,13)
# prs.Slides(1).Shapes.AddPicture(current_path+add_image,0,-1,100,13)

print(prs.Slides(2).Shapes(2).Left)
print(prs.Slides(2).Shapes(2).Height)
print(prs.Slides(2).Shapes(2).Top)
print(prs.Slides(2).Shapes(2).Width)

prs.SaveAs("D:\\MyPythonProj\\python_Data_analy\\2021_0629_OBD\\TEST_PPT_templete.pptx")  # Save as
prs.Close()  # Close PowerPoint document
PowerPoint.Quit()  # Close office



# ---------------------------------------------------------------

current_path = os.getcwd().replace('/','\\') + '\\'
add_image = '새로운 표1.png'
image1 = Image.open('새로운 표1.png')
print(image1.info)

prs.Slides(1).Shapes.AddPicture(current_path+add_image,False,True,1,2) # 마지막 2개는 option으로 크기조정에 쓰임. 미기입 시, 원본 사이즈

''' Picture 밝기 변경'''
# prs.Slides(1).Shapes(18).PictureFormat.Brightness = 0.3

''' Picture Position 및 Size 확인'''
print(prs.Slides(1).Shapes(18).Left)
print(prs.Slides(1).Shapes(18).Height)
print(prs.Slides(1).Shapes(18).Top)
print(prs.Slides(1).Shapes(18).Width)

''' shape name 확인'''
slide_num = 0
slide = prs.slides[slide_num]
shapes_list = slide.shapes
shape_index = {} # 리스트 만들기
for i, shape in enumerate(shapes_list): #enumerate : 리스트의 순서(i)와 리스트 값(shape)을 전달
    shape_index[ shape.name ] = i
print(pd.Series(shape_index))

print(prs.Slides(1).Shapes(18).name)
''' '''
#--------------------------------------------------

SL_Count = ppt.Slides.Count # 불러온 ppt 파일의 Slide 수
SL_Shape_Count = ppt.Slides(2).Shapes.Count  # 선택된 ppt 파일의 Shape 수
SL_Shape_Count_1 = ppt.Slides(2).Shapes(1)
print(SL_Count)
print(SL_Shape_Count)
print(type(SL_Shape_Count))
print(SL_Shape_Count_1.name) # Shape name 확인

# Shape 인덱스 확인
shape_index = []
for i in range(1,SL_Shape_Count+1) :
    shape_index.append([ppt.Slides(2).Shapes(i).name, i]) #2차원 리스트
# print(shape_index)
print(pd.DataFrame(shape_index))

ppt.Slides(2).Shapes(1).TextFrame.TextRange.Text = "박한길"
ppt.Slides(2)


#--------------------------------------------------

'''[아래내용] 절대경로 없이 파일명만 적을 경우, 상대경로로 지정되지 않아 오류가 발생함.
하지만 해당 파일명의 파일이 열려 있을 경우, 오류 없이 코드 동작 함.
아래의 SaveAs 파일에서 파일명만 입력한 경우에 해당 pptx 파일의 경로에 SaveAs 파일명의 파일이 저장됨.
Open 파일이 절대 경로일 경우, SaveAS 파일명만 적을 시, "C:\\Users\\Administrator\\Documents\\"의 경로에 저장됨
[결론] 혼란을 방지코자 무조건 절대 경로를 적어주자.'''
pptSel = ppt.Presentations.Open("D:\\MyPythonProj\\python_Data_analy\\2021_0629_OBD\\test.pptx")
ppt.ActivePresentation.ApplyTheme("C:\\Users\\Administrator\\AppData\\Roaming\\Microsoft\\Templates\\Document Themes\\Default Theme.thmx")
# ppt.ActivePresentation.PageSetup.SlideSize("ppSlideSizeA4Paper")
# ppt.ActivePresentation.PageSetup.SlideWidth - 10
# ppt.ActivePresentation.PageSetup.SlideHeight - 10
ppt.ActivePresentation.PageSetup.SlideSize = 0x03 # A4 size로 변경

# pptSel.Slides(2).Copy()
# pageNums = 10
#
# for i in range(pageNums):
#     pptSel.Slides.Paste()

slide_layout1 = ppt.ActivePresentation.Designs(1).SlideMaster.CustomLayouts(1)
slide_layout2 = ppt.ActivePresentation.Designs(1).SlideMaster.CustomLayouts(2)
print(ppt.ActivePresentation.Designs(1).SlideMaster.CustomLayouts(1).Name)
print(ppt.ActivePresentation.Designs(1).SlideMaster.CustomLayouts(2).Index)
print(ppt.ActivePresentation.Slides.Count) # python-pptx로 작성한 Silide 수 확인

ppt.ActivePresentation.Slides.AddSlide(1,slide_layout1)
ppt.ActivePresentation.Slides.AddSlide(2,slide_layout2)
ppt.ActivePresentation.Slides.AddSlide(2,slide_layout2) # 첫 인자 index는 어느 슬라이드에 추가할지를 결정함.

ppt.ActivePresentation.Slides(4).Layout = 3
ppt.ActivePresentation.Slides(4).CustomLayout = slide_layout1
